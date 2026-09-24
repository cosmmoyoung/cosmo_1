from conftest import make_account, make_order, make_quote, make_thesis

from tradebot.risk.engine import RiskEngine


def check(settings, order=None, thesis="default", account=None, quote="default", buys_today=0,
          docs_cleared=None, industries=None):
    engine = RiskEngine(settings, settings.stop_file)
    return engine.check(
        order or make_order(),
        make_thesis() if thesis == "default" else thesis,
        account or make_account(),
        make_quote() if quote == "default" else quote,
        buys_today=buys_today,
        docs_cleared=docs_cleared or {},
        industries=industries or {"ABC": "Semiconductors"},
    )


def violations(decision) -> str:
    return " | ".join(decision.violations)


def test_clean_buy_passes(settings):
    decision = check(settings)
    assert decision.approved, violations(decision)


def test_stop_file_blocks_everything(settings):
    settings.data_path.mkdir(parents=True)
    settings.stop_file.write_text("stop")
    assert not check(settings).approved
    sell = make_order(side="SELL", quantity=10)
    assert not check(settings, order=sell, account=make_account(positions={"ABC": (10, 100.0)})).approved


def test_position_limit(settings):
    big = make_order(quantity=900)  # 90k of a 1m account = 9% > 8%
    assert "单票仓位" in violations(check(settings, order=big))


def test_industry_limit_counts_other_names(settings):
    account = make_account(cash=700_000, positions={"XYZ": (3_000, 100.0)})  # 30% already in the industry
    decision = check(settings, account=account, industries={"ABC": "Semiconductors", "XYZ": "Semiconductors"})
    assert "行业仓位" in violations(decision)


def test_no_leverage_by_default(settings):
    account = make_account(cash=5_000, positions={"XYZ": (9_950, 100.0)})
    assert "现金" in violations(check(settings, account=account, industries={"XYZ": "Software"}))


def test_research_gate(settings):
    assert "不在允许范围" in violations(check(settings, thesis=make_thesis(reviewer_verdict="REVISE_AND_RESUBMIT")))
    assert "开仓门槛" in violations(check(settings, thesis=make_thesis(conviction=65)))
    assert "不是 active" in violations(check(settings, thesis=make_thesis(status="watch")))
    assert "没有对应的 thesis" in violations(check(settings, thesis=None))


def test_uncleared_expert_call_blocks_buy(settings):
    thesis = make_thesis(evidence_doc_ids=["doc-expert"])
    decision = check(settings, thesis=thesis, docs_cleared={"doc-expert": False})
    assert "合规" in violations(decision)
    assert check(settings, thesis=thesis, docs_cleared={"doc-expert": True}).approved


def test_fat_finger_and_max_entry_price(settings):
    assert "乌龙指" in violations(check(settings, order=make_order(price=110.0)))
    assert "最高买入价" in violations(check(settings, quote=make_quote(price=112.0),
                                            order=make_order(price=112.0)))


def test_daily_loss_and_order_count(settings):
    assert "今日亏损" in violations(check(settings, account=make_account(day_pnl_pct=-3.5)))
    assert "上限" in violations(check(settings, buys_today=10))


def test_sell_only_checks_holdings(settings):
    account = make_account(positions={"ABC": (50, 100.0)})
    assert check(settings, order=make_order(side="SELL", quantity=50), account=account,
                 thesis=make_thesis(status="closed", conviction=0)).approved
    assert "超过持仓" in violations(check(settings, order=make_order(side="SELL", quantity=60), account=account))


def test_missing_quote_blocks(settings):
    assert "报价" in violations(check(settings, quote=None))
