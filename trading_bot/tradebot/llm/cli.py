"""Subscription providers: drive the official `claude` (Claude Code) and `codex` (Codex CLI) tools.

A flat-rate plan (Claude Max, ChatGPT Pro) is far cheaper per token than the API for
heavy, non-urgent work such as deep dives, as long as the usage fits the plan's
limits. The rules this module follows:

- It runs the unmodified official binaries, signed in with *your* account, and never
  reads or reuses their login tokens. Anthropic forbids using subscription credentials
  inside third-party programs; running the official `claude` binary is allowed.
- API keys are removed from the child environment, so the CLI bills the subscription
  instead of silently falling back to pay-per-token API billing.
- Every run happens in an empty temporary directory, with no tools that write files or
  run commands; deep dives get web search only.
- A "usage limit reached" error raises LLMQuotaExceeded, so the bot can pause deep dives
  and retry after the window resets.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from pydantic import ValidationError

from tradebot.config import CLIConfig, LLMTask
from tradebot.llm import LLMError, LLMQuotaExceeded, T, Usage
from tradebot.llm.responses_api import REASONING_EFFORT, extract_json, strict_json_schema

QUOTA_PATTERN = re.compile(
    r"usage.?limit|limit (?:reached|exceeded)|rate.?limit|quota|credits? (?:depleted|exhausted)|\b429\b", re.I,
)
AUTH_PATTERN = re.compile(r"not logged in|please (?:run )?/?login|authenticat|credential|invalid api key|\b401\b", re.I)
API_KEY_VARS = {
    "claude": ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"),
    "codex": ("OPENAI_API_KEY", "CODEX_API_KEY"),
}
BRIDGE_PROMPT = "Complete the task described in the input below."


@dataclass
class RunResult:
    returncode: int
    stdout: str
    stderr: str


# (argv, stdin text, working directory, environment, timeout seconds) -> RunResult
Runner = Callable[[list[str], str, Path, dict[str, str], float], RunResult]


def run_subprocess(argv: list[str], stdin: str, cwd: Path, env: dict[str, str], timeout: float) -> RunResult:
    try:
        proc = subprocess.run(argv, input=stdin, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
    except FileNotFoundError as exc:
        raise LLMError(f"找不到命令 {argv[0]}：请先安装并登录（见 README 的混合方案一节）") from exc
    except subprocess.TimeoutExpired as exc:
        raise LLMError(f"{argv[0]} 超过 {timeout / 60:.0f} 分钟没有返回") from exc
    return RunResult(proc.returncode, proc.stdout, proc.stderr)


def subscription_env(tool: str, strip_api_keys: bool) -> dict[str, str]:
    env = dict(os.environ)
    if strip_api_keys:
        for var in API_KEY_VARS[tool]:
            env.pop(var, None)
    return env


def classify_failure(tool: str, text: str) -> LLMError:
    snippet = " ".join(text.split())[:300] or "(no output)"
    if QUOTA_PATTERN.search(text):
        return LLMQuotaExceeded(f"{tool} 订阅额度用完或被限速：{snippet}")
    if AUTH_PATTERN.search(text):
        return LLMError(f"{tool} 没有登录订阅账号（运行 {tool} 登录一次）：{snippet}")
    return LLMError(f"{tool} 运行失败：{snippet}")


def _validate(schema: type[T], payload: Any, tool: str) -> T:
    try:
        return schema.model_validate(payload)
    except ValidationError as exc:
        raise LLMError(f"{tool} 返回的 {schema.__name__} 格式不对：{exc}") from exc


class ClaudeCLIProvider:
    """`claude -p` (Claude Code headless mode) on your Claude subscription."""

    tool = "claude"

    def __init__(self, cfg: CLIConfig, runner: Runner = run_subprocess):
        self.cfg = cfg
        self.runner = runner
        self.last_usage: Usage | None = None

    def argv(self, task: LLMTask, system: str, *, search: bool, schema: dict | None) -> list[str]:
        # Never add --bare here: bare mode ignores the subscription login and requires an API key.
        tools = "WebSearch,WebFetch" if search else ""
        argv = [
            self.cfg.claude_path, "-p", BRIDGE_PROMPT,
            "--output-format", "json",
            "--model", task.model,
            "--system-prompt", system,
            "--tools", tools,
            "--permission-mode", "dontAsk",
            "--strict-mcp-config",
            "--no-session-persistence",
        ]
        if search:
            argv += ["--allowedTools", tools]
        if task.effort:
            argv += ["--effort", task.effort]
        if schema is not None:
            argv += ["--json-schema", json.dumps(schema, ensure_ascii=False)]
        return argv

    def _run(self, task: LLMTask, system: str, prompt: str, *, search: bool, schema: dict | None) -> dict:
        argv = self.argv(task, system, search=search, schema=schema)
        with tempfile.TemporaryDirectory(prefix="tradebot-claude-") as tmp:
            result = self.runner(argv, prompt, Path(tmp), subscription_env(self.tool, self.cfg.use_subscription_login),
                                 self.cfg.timeout_minutes * 60)
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError:
            raise classify_failure(self.tool, result.stdout + "\n" + result.stderr) from None
        usage = data.get("usage") or {}
        cache_read = usage.get("cache_read_input_tokens") or 0
        cache_write = usage.get("cache_creation_input_tokens") or 0
        self.last_usage = Usage(
            input_tokens=(usage.get("input_tokens") or 0) + cache_read + cache_write,
            cached_input_tokens=cache_read,
            output_tokens=usage.get("output_tokens") or 0,
            cost_usd=data.get("total_cost_usd"),  # Claude Code's API-equivalent estimate
        )
        if result.returncode != 0 or data.get("is_error"):
            raise classify_failure(self.tool, f"{data.get('result') or ''} {result.stderr}")
        return data

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        # The JSON instruction keeps the text reply parseable in case structured_output comes back empty.
        prompt += "\n\nReturn the final answer as one JSON object that matches the provided JSON schema."
        data = self._run(task, system, prompt, search=search, schema=schema.model_json_schema())
        payload = data.get("structured_output")
        if payload is None:
            try:
                payload = extract_json(str(data.get("result") or ""))
            except ValueError as exc:
                raise LLMError(f"claude 没有返回 JSON：{exc}") from exc
        return _validate(schema, payload, self.tool)

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        return str(self._run(task, system, prompt, search=search, schema=None).get("result") or "").strip()


class CodexCLIProvider:
    """`codex exec` (Codex CLI non-interactive mode) on your ChatGPT subscription."""

    tool = "codex"

    def __init__(self, cfg: CLIConfig, runner: Runner = run_subprocess):
        self.cfg = cfg
        self.runner = runner
        self.last_usage: Usage | None = None

    def argv(self, task: LLMTask, workdir: Path, *, search: bool, schema_file: Path | None) -> list[str]:
        argv = [
            self.cfg.codex_path, "exec",
            "--model", task.model,
            "--sandbox", "read-only",
            "--skip-git-repo-check",
            "--ephemeral",
            "--json",
            "--color", "never",
            "--output-last-message", str(workdir / "last_message.txt"),
        ]
        if search:
            argv += ["-c", 'web_search="live"']
        if task.effort:
            argv += ["-c", f'model_reasoning_effort="{REASONING_EFFORT[task.effort]}"']
        if schema_file is not None:
            argv += ["--output-schema", str(schema_file)]
        return argv + ["-"]  # the prompt comes from stdin

    def _run(self, task: LLMTask, system: str, prompt: str, *, search: bool, schema: dict | None) -> str:
        with tempfile.TemporaryDirectory(prefix="tradebot-codex-") as tmp:
            workdir = Path(tmp)
            schema_file = None
            if schema is not None:
                schema_file = workdir / "schema.json"
                schema_file.write_text(json.dumps(schema, ensure_ascii=False), encoding="utf-8")
            argv = self.argv(task, workdir, search=search, schema_file=schema_file)
            stdin = f"<instructions>\n{system}\n</instructions>\n\n{prompt}"
            result = self.runner(argv, stdin, workdir, subscription_env(self.tool, self.cfg.use_subscription_login),
                                 self.cfg.timeout_minutes * 60)
            events = _jsonl(result.stdout)
            self.last_usage = sum((_codex_usage(e) for e in events if e.get("type") == "turn.completed"), Usage())
            if result.returncode != 0 or any(e.get("type") == "turn.failed" for e in events):
                # "error" events can also be retried hiccups, so they only add detail to a real failure.
                detail = " ".join(_codex_error(e) for e in events if e.get("type") in ("turn.failed", "error"))
                raise classify_failure(self.tool, f"{detail} {result.stderr}")
            last = workdir / "last_message.txt"
            if last.exists():
                return last.read_text(encoding="utf-8").strip()
        messages = [e["item"].get("text", "") for e in events
                    if e.get("type") == "item.completed" and (e.get("item") or {}).get("type") == "agent_message"]
        if not messages:
            raise LLMError("codex 没有返回任何内容")
        return messages[-1].strip()

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        reply = self._run(task, system, prompt, search=search, schema=strict_json_schema(schema))
        try:
            payload = extract_json(reply)
        except ValueError as exc:
            raise LLMError(f"codex 没有返回 JSON：{exc}") from exc
        return _validate(schema, payload, self.tool)

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        return self._run(task, system, prompt, search=search, schema=None)


def _jsonl(text: str) -> list[dict]:
    events = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue  # progress lines and warnings are not events
        if isinstance(event, dict):
            events.append(event)
    return events


def _codex_usage(event: dict) -> Usage:
    usage = event.get("usage") or {}
    return Usage(
        input_tokens=usage.get("input_tokens") or 0,
        cached_input_tokens=usage.get("cached_input_tokens") or 0,
        output_tokens=usage.get("output_tokens") or 0,
    )


def _codex_error(event: dict) -> str:
    error = event.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error)
    return str(error or event.get("message") or "")
