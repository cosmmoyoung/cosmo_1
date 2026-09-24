import json

from tradebot.config import LLMTask
from tradebot.doctor import FAIL, OK, WARN, Ping, live_checks, run_checks
from tradebot.llm import LLMRouter
from tradebot.llm.cli import RunResult
from tradebot.llm.fake import FakeProvider

ENV = {"FMP_API_KEY": "f", "OPENAI_API_KEY": "o", "ANTHROPIC_API_KEY": "a"}


def runner_for(auth_status: dict | None = None, codex_status: str = "Logged in using ChatGPT"):
    seen = []

    def run(argv, stdin, cwd, env, timeout):
        seen.append((argv, env))
        if argv[1:] == ["--version"]:
            return RunResult(0, "1.0 (test)", "")
        if argv[1:3] == ["auth", "status"]:
            return RunResult(0, json.dumps(auth_status or {}), "")
        if argv[1:3] == ["login", "status"]:
            return RunResult(0, codex_status, "")
        raise AssertionError(argv)

    run.seen = seen
    return run


def statuses(checks):
    return {c.item.split("（")[0]: c.status for c in checks}


def test_default_hybrid_config_all_green(settings):
    runner = runner_for({"loggedIn": True, "authMethod": "claude.ai"})
    checks = run_checks(settings, runner=runner, which=lambda name: f"/usr/bin/{name}", env=ENV)
    s = statuses(checks)
    assert s["FMP"] == OK and s["OpenAI API"] == OK and s["Claude Code 订阅通道"] == OK
    auth_env = next(env for argv, env in runner.seen if argv[1:3] == ["auth", "status"])
    assert "ANTHROPIC_API_KEY" not in auth_env  # checks the login the bot will actually use


def test_claude_cli_problems(settings):
    missing = run_checks(settings, runner=runner_for(), which=lambda name: None, env=ENV)
    assert statuses(missing)["Claude Code 订阅通道"] == FAIL
    logged_out = run_checks(settings, runner=runner_for({"loggedIn": False}), which=lambda n: "/x", env=ENV)
    assert statuses(logged_out)["Claude Code 订阅通道"] == FAIL
    api_key = run_checks(settings, runner=runner_for({"loggedIn": True, "authMethod": "api_key"}), which=lambda n: "/x", env=ENV)
    assert statuses(api_key)["Claude Code 订阅通道"] == WARN


def test_codex_login_states(settings):
    settings.llm.research = LLMTask(provider="codex_cli", model="gpt-6-astra")
    settings.llm.synthesis = LLMTask(provider="codex_cli", model="gpt-6-astra")
    for text, expected in (("Logged in using ChatGPT", OK), ("Logged in using an API key", WARN), ("Not logged in", FAIL)):
        checks = run_checks(settings, runner=runner_for(codex_status=text), which=lambda n: "/x", env=ENV)
        assert statuses(checks)["Codex 订阅通道"] == expected, text


def test_missing_keys_fail(settings):
    checks = run_checks(settings, runner=runner_for({"loggedIn": True, "authMethod": "claude.ai"}),
                        which=lambda n: "/x", env={})
    s = statuses(checks)
    assert s["FMP"] == FAIL and s["OpenAI API"] == FAIL


def test_live_checks_ping_each_model(settings):
    for stage in settings.llm.STAGES:
        getattr(settings.llm, stage).provider = "fake"
    fake = FakeProvider({"Ping": lambda system, prompt: Ping(ok=True)})
    checks = live_checks(settings, LLMRouter(settings.llm, {"fake": fake}))
    assert checks and all(c.status == OK for c in checks)
    assert len(checks) == len({(getattr(settings.llm, s).model) for s in settings.llm.STAGES if s != "scout"})
