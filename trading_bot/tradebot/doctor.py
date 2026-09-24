"""`tradebot doctor`: check keys, command-line tools, logins and the broker before running.

The static checks cost nothing. `--live` also sends one tiny request through every
model the config uses (a few cents on the API, a sliver of subscription quota).
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from pydantic import BaseModel

from tradebot.config import LLMTask, Settings
from tradebot.llm import LLMRouter
from tradebot.llm.cli import Runner, run_subprocess, subscription_env

OK, WARN, FAIL = "ok", "warn", "fail"
ICONS = {OK: "✅", WARN: "⚠️ ", FAIL: "❌"}


@dataclass
class Check:
    status: str
    item: str
    detail: str

    def line(self) -> str:
        return f"{ICONS[self.status]} {self.item}：{self.detail}"


def _stages_using(settings: Settings, provider: str) -> str:
    stages = [s for s in settings.llm.STAGES if getattr(settings.llm, s).provider == provider]
    return "、".join(stages) or "fallback"


def _key(env: dict[str, str], names: tuple[str, ...], item: str, detail: str, missing_status: str = FAIL) -> Check:
    found = next((n for n in names if env.get(n)), None)
    if found:
        return Check(OK, item, f"{found} 已设置")
    return Check(missing_status, item, f"缺少 {' 或 '.join(names)}。{detail}")


def _run(runner: Runner, argv: list[str], env: dict[str, str]) -> tuple[int, str]:
    with tempfile.TemporaryDirectory(prefix="tradebot-doctor-") as tmp:
        try:
            result = runner(argv, "", Path(tmp), env, 60)
        except Exception as exc:  # a broken CLI should show up as a failed check, not a crash
            return 1, str(exc)
    return result.returncode, (result.stdout + result.stderr).strip()


def claude_cli_checks(settings: Settings, runner: Runner, which: Callable[[str], str | None],
                      env: dict[str, str]) -> list[Check]:
    cfg = settings.llm.cli
    item = f"Claude Code 订阅通道（{_stages_using(settings, 'claude_cli')}）"
    path = which(cfg.claude_path)
    if not path:
        return [Check(FAIL, item, "没找到 claude 命令。安装 Claude Code 后运行一次 claude，输入 /login 登录你的订阅账号")]
    _, version = _run(runner, [path, "--version"], env)
    _, out = _run(runner, [path, "auth", "status", "--json"], subscription_env("claude", cfg.use_subscription_login))
    try:
        status = json.loads(out)
    except json.JSONDecodeError:
        return [Check(FAIL, item, f"读不到登录状态（{out[:120]}）")]
    checks = []
    if not status.get("loggedIn"):
        checks.append(Check(FAIL, item, f"{version}，但没有登录。运行 claude，输入 /login 登录你的 Claude 订阅"))
    elif "api" in str(status.get("authMethod", "")).lower():
        checks.append(Check(WARN, item, f"{version}，当前用 API key 登录（{status.get('authMethod')}），会按 token 计费，不走订阅"))
    else:
        checks.append(Check(OK, item, f"{version}，已登录（{status.get('authMethod')}）"))
    if cfg.use_subscription_login and any(env.get(k) for k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")):
        checks.append(Check(OK, "Claude API key", "环境里有 API key；机器人调用 claude 时会把它去掉，确保走订阅"))
    return checks


def codex_cli_checks(settings: Settings, runner: Runner, which: Callable[[str], str | None],
                     env: dict[str, str]) -> list[Check]:
    cfg = settings.llm.cli
    item = f"Codex 订阅通道（{_stages_using(settings, 'codex_cli')}）"
    path = which(cfg.codex_path)
    if not path:
        return [Check(FAIL, item, "没找到 codex 命令。运行 npm install -g @openai/codex，然后 codex login 选择用 ChatGPT 登录")]
    _, version = _run(runner, [path, "--version"], env)
    _, out = _run(runner, [path, "login", "status"], subscription_env("codex", cfg.use_subscription_login))
    lowered = out.lower()
    if "chatgpt" in lowered:
        return [Check(OK, item, f"{version}，{out.splitlines()[0]}")]
    if "api key" in lowered:
        return [Check(WARN, item, f"{version}，当前用 API key 登录，会按 token 计费。运行 codex login 改用 ChatGPT 登录")]
    return [Check(FAIL, item, f"{version}，没有登录。运行 codex login，选择用 ChatGPT 登录")]


def run_checks(settings: Settings, runner: Runner = run_subprocess,
               which: Callable[[str], str | None] = shutil.which, env: dict[str, str] | None = None) -> list[Check]:
    env = dict(os.environ if env is None else env)
    providers = settings.llm.providers_in_use(include_scout=settings.sources.grok_scout)
    checks = [_key(env, ("FMP_API_KEY",), "FMP（新闻、报价、财务数据）", "在 .env 里填写")]
    if "openai" in providers:
        checks.append(_key(env, ("OPENAI_API_KEY",), f"OpenAI API（{_stages_using(settings, 'openai')}）",
                           "在 .env 里填写，或把这些环节改成别的通道"))
    if "claude" in providers:
        checks.append(_key(env, ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"),
                           f"Claude API（{_stages_using(settings, 'claude')}）",
                           "在 .env 里填写（用 ant auth login 登录过也可以）", missing_status=WARN))
    if "grok" in providers:
        checks.append(_key(env, ("XAI_API_KEY",), "Grok（X 新闻侦察）", "在 .env 里填写，或关掉 sources.grok_scout"))
    if "claude_cli" in providers:
        checks += claude_cli_checks(settings, runner, which, env)
    if "codex_cli" in providers:
        checks += codex_cli_checks(settings, runner, which, env)

    ex = settings.execution
    if ex.broker == "ibkr":
        if importlib.util.find_spec("ib_async") is None:
            checks.append(Check(FAIL, "券商", "IBKR 需要 ib_async：pip install -e '.[ibkr]'"))
        else:
            live = ex.ibkr_port in (7496, 4001)
            checks.append(Check(WARN if live else OK, "券商", f"IBKR {'实盘' if live else '模拟盘'}端口 {ex.ibkr_port}"))
    else:
        checks.append(Check(OK, "券商", "模拟盘（paper）"))
    checks.append(Check(OK if ex.approval == "manual" else WARN, "下单审批",
                        "每一单都要你批准" if ex.approval == "manual" else "风控通过就自动下单"))
    if settings.stop_file.exists():
        checks.append(Check(WARN, "紧急停止", "STOP 文件存在，机器人不会下单（tradebot resume 解除）"))
    return checks


class Ping(BaseModel):
    ok: bool


def live_checks(settings: Settings, router: LLMRouter) -> list[Check]:
    """One tiny structured request per distinct (provider, model) in the config."""
    checks, seen = [], set()
    for stage in settings.llm.STAGES:
        if stage == "scout" and not settings.sources.grok_scout:
            continue
        task: LLMTask = getattr(settings.llm, stage)
        if (task.provider, task.model) in seen:
            continue
        seen.add((task.provider, task.model))
        item = f"实测 {task.provider} / {task.model}"
        started = time.monotonic()
        try:
            reply = router.with_stages(triage=task).structured(
                "triage", "You are a connectivity check.", "Return ok = true.", Ping)
            status = OK if reply.ok else WARN
            checks.append(Check(status, item, f"{time.monotonic() - started:.0f} 秒返回"))
        except Exception as exc:
            checks.append(Check(FAIL, item, f"{type(exc).__name__}: {str(exc)[:200]}"))
    return checks
