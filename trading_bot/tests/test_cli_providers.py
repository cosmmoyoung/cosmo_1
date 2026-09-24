"""The subscription providers, with a fake runner in place of the real `claude` / `codex` binaries."""

import json

import pytest

from tradebot.config import CLIConfig, LLMTask
from tradebot.llm import LLMError, LLMQuotaExceeded
from tradebot.llm.cli import ClaudeCLIProvider, CodexCLIProvider, RunResult
from tradebot.models import TriageBatch

TRIAGE = {"results": [{
    "item_id": "n1", "materiality": 7, "tickers": ["TSM"], "industries": ["Semiconductors"],
    "event_type": "guidance", "summary": "raised guidance", "route": "thesis_check",
}]}


class FakeRunner:
    def __init__(self, respond):
        self.respond = respond
        self.calls = []

    def __call__(self, argv, stdin, cwd, env, timeout):
        self.calls.append({"argv": argv, "stdin": stdin, "cwd": cwd, "env": env, "timeout": timeout})
        return self.respond(argv, cwd)


@pytest.fixture(autouse=True)
def api_keys(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-should-not-leak")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-openai-should-not-leak")
    monkeypatch.setenv("CLAUDE_CODE_OAUTH_TOKEN", "subscription-token")


def claude_reply(payload: dict, returncode: int = 0):
    return lambda argv, cwd: RunResult(returncode, json.dumps(payload), "")


def test_claude_structured_uses_subscription_and_schema():
    runner = FakeRunner(claude_reply({
        "type": "result", "is_error": False, "result": "", "structured_output": TRIAGE, "total_cost_usd": 0.42,
        "usage": {"input_tokens": 100, "cache_read_input_tokens": 900, "cache_creation_input_tokens": 50, "output_tokens": 70},
    }))
    provider = ClaudeCLIProvider(CLIConfig(), runner)
    result = provider.structured(LLMTask(provider="claude_cli", model="opus", effort="high"), "SYSTEM", "PROMPT", TriageBatch)

    call = runner.calls[0]
    argv = call["argv"]
    assert result.results[0].tickers == ["TSM"]
    assert argv[:3] == ["claude", "-p", argv[2]] and "--bare" not in argv
    assert argv[argv.index("--output-format") + 1] == "json"
    assert argv[argv.index("--model") + 1] == "opus"
    assert argv[argv.index("--effort") + 1] == "high"
    assert argv[argv.index("--system-prompt") + 1] == "SYSTEM"
    assert argv[argv.index("--tools") + 1] == ""  # no tools at all for a structured call
    assert json.loads(argv[argv.index("--json-schema") + 1])["title"] == "TriageBatch"
    assert call["stdin"].startswith("PROMPT") and "JSON" in call["stdin"]
    assert "ANTHROPIC_API_KEY" not in call["env"]  # bills the subscription, not the API
    assert call["env"]["CLAUDE_CODE_OAUTH_TOKEN"] == "subscription-token"
    assert provider.last_usage.input_tokens == 1050 and provider.last_usage.cached_input_tokens == 900
    assert provider.last_usage.cost_usd == 0.42


def test_claude_structured_falls_back_to_json_text():
    runner = FakeRunner(claude_reply({"is_error": False, "result": "```json\n" + json.dumps(TRIAGE) + "\n```", "usage": {}}))
    result = ClaudeCLIProvider(CLIConfig(), runner).structured(
        LLMTask(provider="claude_cli", model="opus"), "S", "P", TriageBatch)
    assert result.results[0].item_id == "n1"


def test_claude_text_with_web_search():
    runner = FakeRunner(claude_reply({"is_error": False, "result": "  memo  ", "usage": {}}))
    memo = ClaudeCLIProvider(CLIConfig(), runner).text(LLMTask(provider="claude_cli", model="opus"), "S", "P", search=True)
    argv = runner.calls[0]["argv"]
    assert memo == "memo"
    assert argv[argv.index("--tools") + 1] == "WebSearch,WebFetch"
    assert argv[argv.index("--allowedTools") + 1] == "WebSearch,WebFetch"


def test_claude_usage_limit_is_a_quota_error():
    runner = FakeRunner(claude_reply({"is_error": True, "result": "Claude AI usage limit reached|1760000000"}, 1))
    with pytest.raises(LLMQuotaExceeded):
        ClaudeCLIProvider(CLIConfig(), runner).text(LLMTask(provider="claude_cli", model="opus"), "S", "P")


def test_claude_not_logged_in_is_a_plain_error():
    runner = FakeRunner(lambda argv, cwd: RunResult(1, "Invalid API key · Please run /login", ""))
    with pytest.raises(LLMError) as exc:
        ClaudeCLIProvider(CLIConfig(), runner).text(LLMTask(provider="claude_cli", model="opus"), "S", "P")
    assert not isinstance(exc.value, LLMQuotaExceeded)


def codex_reply(message: str, events: list[dict], returncode: int = 0):
    def respond(argv, cwd):
        out = argv[argv.index("--output-last-message") + 1]
        if message:
            (cwd / "last_message.txt").write_text(message, encoding="utf-8")
            assert out == str(cwd / "last_message.txt")
        return RunResult(returncode, "\n".join(json.dumps(e) for e in events), "")
    return respond


def test_codex_structured_request_shape():
    seen = {}

    def respond(argv, cwd):
        schema_file = argv[argv.index("--output-schema") + 1]
        with open(schema_file, encoding="utf-8") as fh:
            seen["schema"] = json.load(fh)
        return codex_reply(json.dumps(TRIAGE), [
            {"type": "thread.started"},
            {"type": "turn.completed", "usage": {"input_tokens": 5000, "cached_input_tokens": 1000, "output_tokens": 800}},
        ])(argv, cwd)

    runner = FakeRunner(respond)
    provider = CodexCLIProvider(CLIConfig(), runner)
    result = provider.structured(LLMTask(provider="codex_cli", model="gpt-6-astra", effort="max"), "SYSTEM", "PROMPT", TriageBatch)

    call = runner.calls[0]
    argv = call["argv"]
    assert result.results[0].item_id == "n1"
    assert argv[:2] == ["codex", "exec"] and argv[-1] == "-"
    assert argv[argv.index("--model") + 1] == "gpt-6-astra"
    assert argv[argv.index("--sandbox") + 1] == "read-only"
    for flag in ("--skip-git-repo-check", "--ephemeral", "--json"):
        assert flag in argv
    assert 'model_reasoning_effort="xhigh"' in argv
    assert 'web_search="live"' not in argv
    assert seen["schema"]["additionalProperties"] is False
    assert call["stdin"].startswith("<instructions>\nSYSTEM\n</instructions>") and call["stdin"].endswith("PROMPT")
    assert "OPENAI_API_KEY" not in call["env"]
    assert (provider.last_usage.input_tokens, provider.last_usage.cached_input_tokens, provider.last_usage.output_tokens) == (5000, 1000, 800)


def test_codex_text_with_search_and_message_fallback():
    runner = FakeRunner(codex_reply("", [
        {"type": "item.completed", "item": {"type": "agent_message", "text": "research memo"}},
        {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}},
    ]))
    memo = CodexCLIProvider(CLIConfig(), runner).text(LLMTask(provider="codex_cli", model="gpt-6-sol"), "S", "P", search=True)
    assert memo == "research memo"
    assert 'web_search="live"' in runner.calls[0]["argv"]


def test_codex_usage_limit_is_a_quota_error():
    runner = FakeRunner(codex_reply("", [
        {"type": "turn.failed", "error": {"message": "You've hit your usage limit. Try again in 2 hours."}},
    ], returncode=1))
    with pytest.raises(LLMQuotaExceeded):
        CodexCLIProvider(CLIConfig(), runner).text(LLMTask(provider="codex_cli", model="gpt-6-astra"), "S", "P")


def test_api_keys_kept_when_subscription_login_disabled():
    runner = FakeRunner(claude_reply({"is_error": False, "result": "ok", "usage": {}}))
    ClaudeCLIProvider(CLIConfig(use_subscription_login=False), runner).text(LLMTask(provider="claude_cli", model="opus"), "S", "P")
    assert runner.calls[0]["env"]["ANTHROPIC_API_KEY"] == "sk-ant-should-not-leak"
