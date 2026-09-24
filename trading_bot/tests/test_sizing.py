from conftest import make_account, make_quote, make_thesis

from tradebot.models import utcnow
from tradebot.risk.sizing import limit_price, plan_order, target_weight_pct


def test_target_weight_curve(settings):
    assert target_weight_pct(49, settings) == 0.0
    assert target_weight_pct(50, settings) == 0.0
    assert target_weight_pct(70, settings) == 3.56
    assert target_weight_pct(95, settings) == 8.0
    assert target_weight_pct(100, settings) == 8.0


def test_limit_price_offsets():
    assert limit_price("BUY", 100.0, 0.3) == 100.3
    assert limit_price("SELL", 100.0, 0.3) == 99.7


def test_opens_position_toward_target(settings):
    order = plan_order(make_thesis(conviction=80), make_account(), make_quote(price=100.0), settings, utcnow())
    assert order.side == "BUY"
    assert order.quantity == 533  # 5.33% of 1m at $100
    assert "开仓" in order.reason


def test_no_new_position_below_open_conviction(settings):
    assert plan_order(make_thesis(conviction=65), make_account(), make_quote(), settings, utcnow()) is None


def test_waits_when_price_above_max_entry(settings):
    thesis = make_thesis(conviction=85, max_entry_price=90.0)
    assert plan_order(thesis, make_account(), make_quote(price=100.0), settings, utcnow()) is None


def test_band_prevents_churn(settings):
    account = make_account(cash=950_000, positions={"ABC": (500, 100.0)})  # 5.0% held, target 5.33%
    assert plan_order(make_thesis(conviction=80), account, make_quote(), settings, utcnow()) is None


def test_trims_when_conviction_falls(settings):
    account = make_account(cash=930_000, positions={"ABC": (700, 100.0)})  # 7% held
    order = plan_order(make_thesis(conviction=60), account, make_quote(), settings, utcnow())
    assert order.side == "SELL" and "减仓" in order.reason
    assert 0 < order.quantity < 700


def test_closed_thesis_sells_everything(settings):
    account = make_account(cash=950_000, positions={"ABC": (500, 100.0)})
    order = plan_order(make_thesis(status="closed", conviction=0), account, make_quote(), settings, utcnow())
    assert order.side == "SELL" and order.quantity == 500 and "清仓" in order.reason
