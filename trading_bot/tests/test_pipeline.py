"""End to end on fake data: news -> research -> order -> approval -> news -> exit."""

import json
from datetime import timedelta

from tradebot.demo import BAD_NEWS, TICKER, DemoFMP, ScriptedNews, demo_news, demo_provider, demo_settings, run_demo
from tradebot.execution.ibkr import IBKRBroker
from tradebot.models import iso, utcnow
from tradebot.orchestrator import build_bot


def test_demo_runs_the_full_loop(tmp_path):
    bot = run_demo(tmp_path, say=lambda _: None)
    thesis = bot.store.get_thesis(TICKER)
    assert thesis.status == "closed" and thesis.conviction == 0
    orders = bot.store.orders()
    assert sorted((o.side, o.status) for o in orders) == [("BUY", "filled"), ("SELL", "filled")]
    assert bot.broker.account().qty(TICKER) == 0
    assert len(thesis.memo_paths) == 3 and all(p.endswith(".md") for p in thesis.memo_paths)


def make_bot(tmp_path, **settings_overrides):
    settings = demo_settings(tmp_path)
    for section, values in settings_overrides.items():
        for key, value in values.items():
            setattr(getattr(settings, section), key, value)
    provider = demo_provider()
    bot = build_bot(settings, providers={"fake": provider}, fmp=DemoFMP(),
                    news_sources=[ScriptedNews(demo_news())])
    return bot, provider


def test_auto_approval_on_paper(tmp_path):
    bot, _ = make_bot(tmp_path, execution={"approval": "auto"})
    bot.poll_news()
    bot.work_research_queue()
    assert bot.broker.account().qty(TICKER) > 0
    assert not bot.store.orders("pending_approval")


def test_stop_file_halts_cycle_and_approvals(tmp_path):
    bot, provider = make_bot(tmp_path)
    bot.poll_news()
    bot.work_research_queue()
    order = bot.store.orders("pending_approval")[0]
    bot.settings.stop_file.write_text("stop")
    assert bot.cycle() == {"halted": 1}
    assert bot.desk.approve(order.id).status == "rejected"


def test_approval_rechecks_price(tmp_path):
    bot, _ = make_bot(tmp_path)
    bot.poll_news()
    bot.work_research_queue()
    order = bot.store.orders("pending_approval")[0]
    bot.fmp.price = 60.0  # price ran away (and above max entry) before you approved
    result = bot.desk.approve(order.id)
    assert result.status == "rejected"
    assert any("乌龙指" in note or "最高买入价" in note for note in result.risk_notes)


def test_stale_approvals_expire(tmp_path):
    bot, _ = make_bot(tmp_path)
    bot.poll_news()
    bot.work_research_queue()
    order = bot.store.orders("pending_approval")[0]
    order.created_at = iso(utcnow() - timedelta(hours=30))
    bot.store.save_order(order)
    assert bot.desk.expire_stale() == 1
    assert bot.store.get_order(order.id).status == "expired"


def test_deep_dive_budget(tmp_path):
    bot, provider = make_bot(tmp_path, schedule={"max_deep_dives_per_day": 0})
    bot.poll_news()
    assert bot.work_research_queue() == 0
    assert "ThesisDraft" not in provider.calls


def test_news_is_triaged_once(tmp_path):
    bot, provider = make_bot(tmp_path)
    bot.poll_news()
    bot.news_sources[0].batches.insert(0, demo_news()[0])  # same headline again
    bot.poll_news()
    assert provider.calls.count("TriageBatch") == 1


def test_uncleared_expert_call_never_reaches_research(tmp_path):
    bot, _ = make_bot(tmp_path)
    notes = bot.settings.path("inbox") / "expert_calls" / "insider.md"
    notes.write_text(f"---\ntickers: [{TICKER}]\n---\nSECRET-DETAIL from a current employee", encoding="utf-8")
    seen_prompts = []
    original = bot.router.text

    def spy(name, system, prompt, search=False):
        seen_prompts.append(prompt)
        return original(name, system, prompt, search=search)

    bot.router.text = spy
    bot.poll_news()
    bot.work_research_queue()
    assert seen_prompts and not any("SECRET-DETAIL" in p for p in seen_prompts)


def test_missing_verdict_line_blocks_trading(tmp_path):
    bot, provider = make_bot(tmp_path)
    provider._text = lambda system, prompt: "memo without a machine-readable verdict"
    bot.poll_news()
    bot.work_research_queue()
    thesis = bot.store.get_thesis(TICKER)
    assert thesis.reviewer_verdict == "REVISE_AND_RESUBMIT" and thesis.status == "watch"
    assert not bot.store.orders()


def test_thesis_news_triggers_exit_order(tmp_path):
    bot, _ = make_bot(tmp_path, execution={"approval": "auto"})
    bot.poll_news()
    bot.work_research_queue()
    bot.poll_news()  # the customer-loss headline
    thesis = bot.store.get_thesis(TICKER)
    assert thesis.status == "closed"
    assert BAD_NEWS in thesis.history[-1].trigger
    assert bot.broker.account().qty(TICKER) == 0


class FakeIB:
    def __init__(self):
        self.placed = []

    def accountSummary(self):
        from types import SimpleNamespace as NS
        return [NS(tag="NetLiquidation", value="7800000", currency="HKD"),
                NS(tag="TotalCashValue", value="3900000", currency="HKD")]

    def accountValues(self):
        from types import SimpleNamespace as NS
        return [NS(tag="ExchangeRate", value="7.8", currency="USD")]

    def portfolio(self):
        from types import SimpleNamespace as NS
        return [
            NS(contract=NS(secType="STK", currency="USD", symbol="TSM"), position=100, averageCost=400.0, marketPrice=450.0),
            NS(contract=NS(secType="STK", currency="HKD", symbol="700"), position=100, averageCost=500.0, marketPrice=520.0),
        ]

    def managedAccounts(self):
        raise RuntimeError("no pnl in tests")


def test_ibkr_account_converts_hkd_base_to_usd(settings):
    settings.execution.ibkr_port = 7497
    broker = IBKRBroker(settings.execution, ib=FakeIB())
    account = broker.account()
    assert round(account.nav) == 1_000_000 and round(account.cash) == 500_000
    assert list(account.positions) == ["TSM"]  # only US stocks are managed
    assert account.day_pnl_pct is None


def test_ibkr_refuses_live_port_without_both_switches(settings, monkeypatch):
    settings.execution.ibkr_port = 7496
    monkeypatch.delenv("TRADEBOT_LIVE", raising=False)
    try:
        IBKRBroker(settings.execution, ib=FakeIB())
    except RuntimeError as exc:
        assert "实盘" in str(exc)
    else:
        raise AssertionError("live port must be refused")
    settings.execution.allow_live = True
    monkeypatch.setenv("TRADEBOT_LIVE", "YES")
    assert IBKRBroker(settings.execution, ib=FakeIB()).is_live


def test_cli_demo_and_status_commands(tmp_path, capsys):
    from tradebot.cli import main

    config = tmp_path / "config.yaml"
    config.write_text(json.dumps({"data_dir": "data", "execution": {"broker": "paper"}}), encoding="utf-8")
    assert main(["-c", str(config), "stop"]) == 0
    assert (tmp_path / "data" / "STOP").exists()
    assert main(["-c", str(config), "resume"]) == 0
    assert main(["-c", str(config), "theses"]) == 0
    assert "还没有 thesis" in capsys.readouterr().out


def test_quota_pauses_research_and_requeues(tmp_path):
    from tradebot.llm import LLMQuotaExceeded

    bot, provider = make_bot(tmp_path)

    def used_up(system, prompt):
        raise LLMQuotaExceeded("claude usage limit reached")

    provider._text = used_up
    bot.poll_news()
    assert bot.work_research_queue() == 0
    assert bot.store.next_idea()["ticker"] == TICKER  # back in the queue, not marked failed
    assert bot.research_paused()
    assert any("订阅额度用完" in m for m in bot.notifier.sent)
    calls_before = len(provider.calls)
    assert bot.work_research_queue() == 0 and len(provider.calls) == calls_before  # waits for the reset


def test_one_deep_dive_per_cycle(tmp_path):
    from tradebot.models import Quote

    bot, _ = make_bot(tmp_path)
    bot.fmp.quote = lambda symbol: Quote(ticker=symbol, price=50.0, market_cap=8e9)  # both are researchable
    bot.store.enqueue_idea(TICKER, "a", "manual", 90)
    bot.store.enqueue_idea("OTHR", "b", "manual", 80)
    assert bot.work_research_queue() == 1
    assert bot.store.next_idea()["ticker"] == "OTHR"  # waits for the next cycle
    assert bot.work_research_queue() == 1


def test_usage_is_logged(tmp_path):
    from tradebot.llm import Usage

    settings = demo_settings(tmp_path)
    provider = demo_provider()
    provider._usage = Usage(input_tokens=2000, cached_input_tokens=0, output_tokens=500)
    bot = build_bot(settings, providers={"fake": provider}, fmp=DemoFMP(), news_sources=[ScriptedNews(demo_news())])
    bot.poll_news()
    bot.work_research_queue()
    rows = bot.store.usage_summary(1)
    assert rows and sum(r["calls"] for r in rows) == len(provider.calls)


def test_compare_does_not_touch_live_thesis(tmp_path):
    from tradebot.config import LLMTask

    bot, _ = make_bot(tmp_path)
    routes = {"alpha": LLMTask(provider="fake", model="m1"), "beta": LLMTask(provider="fake", model="m2")}
    results = bot.compare(TICKER, routes)
    assert set(results) == {"alpha", "beta"}
    assert bot.store.get_thesis(TICKER) is None and not bot.store.orders()
    for label, result in results.items():
        assert result.error is None
        assert all(f"_{label}_" in path for path in result.thesis.memo_paths)


def test_compare_keeps_going_when_one_route_fails(tmp_path):
    from tradebot.config import LLMTask

    bot, _ = make_bot(tmp_path)
    routes = {"missing": LLMTask(provider="codex_cli", model="gpt-6-astra"), "ok": LLMTask(provider="fake", model="m")}
    results = bot.compare(TICKER, routes)
    assert results["missing"].thesis is None and "codex_cli" in results["missing"].error
    assert results["ok"].thesis is not None


def test_cli_usage_command(tmp_path, capsys):
    from tradebot.cli import main
    from tradebot.store import Store

    config = tmp_path / "config.yaml"
    config.write_text("data_dir: data\n", encoding="utf-8")
    store = Store(tmp_path / "data" / "tradebot.db")
    store.record_usage("research", "claude_cli", "opus", "subscription", 100_000, 0, 20_000, 1.0)
    store.record_usage("triage", "openai", "gpt-6-luna", "api", 50_000, 0, 10_000, 0.01)
    assert main(["-c", str(config), "usage"]) == 0
    out = capsys.readouterr().out
    assert "API 实际花费（估算）：$0.01" in out and "$1.00" in out
