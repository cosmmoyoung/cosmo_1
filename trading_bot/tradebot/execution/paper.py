"""Paper broker: simulated account in SQLite, marked to market with live quotes.

Fills are simplified on purpose: a marketable limit order fills in full at the
last price, with an IBKR-style commission. Good enough to test the logic, not
to estimate slippage.
"""

from __future__ import annotations

from typing import Callable

from tradebot.models import AccountSnapshot, OrderResult, Position, Quote, Side, stable_id, utcnow
from tradebot.store import Store


def commission(quantity: int) -> float:
    return max(1.0, 0.005 * quantity)


class PaperBroker:
    name = "paper"
    is_live = False

    def __init__(self, store: Store, quote: Callable[[str], Quote | None], starting_cash: float):
        self.store = store
        self.quote = quote
        self.starting_cash = starting_cash

    def account(self) -> AccountSnapshot:
        cash = self.store.paper_cash(self.starting_cash)
        positions = {}
        for ticker, (qty, avg_cost) in self.store.paper_positions().items():
            quote = self.quote(ticker)
            positions[ticker] = Position(
                ticker=ticker, qty=qty, avg_cost=avg_cost, market_price=quote.price if quote else avg_cost,
            )
        nav = cash + sum(p.value for p in positions.values())
        return AccountSnapshot(nav=nav, cash=cash, positions=positions, day_pnl_pct=self._day_pnl_pct(nav))

    def _day_pnl_pct(self, nav: float) -> float:
        key = f"paper_nav_open:{utcnow().date().isoformat()}"
        opening = self.store.get_meta(key)
        if opening is None:
            self.store.set_meta(key, repr(nav))
            return 0.0
        return 100 * (nav / float(opening) - 1)

    def round_quantity(self, ticker: str, quantity: int) -> int:
        return max(int(quantity), 0)

    def place_limit_order(self, ticker: str, side: Side, quantity: int, limit_price: float) -> OrderResult:
        order_id = f"paper-{stable_id(ticker, side, quantity, utcnow().isoformat())}"
        quote = self.quote(ticker)
        if quote is None:
            return OrderResult(broker_order_id=order_id, status="rejected: no quote")
        marketable = limit_price >= quote.price if side == "BUY" else limit_price <= quote.price
        if not marketable:
            return OrderResult(broker_order_id=order_id, status="cancelled: limit not marketable")
        fill = quote.price
        cash = self.store.paper_cash(self.starting_cash) - commission(quantity)
        held, avg_cost = self.store.paper_positions().get(ticker, (0.0, 0.0))
        if side == "BUY":
            new_qty = held + quantity
            avg_cost = (held * avg_cost + quantity * fill) / new_qty
            cash -= quantity * fill
        else:
            new_qty = held - quantity
            cash += quantity * fill
        self.store.set_paper_position(ticker, new_qty, avg_cost)
        self.store.set_paper_cash(cash)
        return OrderResult(broker_order_id=order_id, status="filled", filled_qty=quantity, avg_price=fill)

    def order_status(self, broker_order_id: str) -> OrderResult | None:
        return None  # paper orders are final the moment they are placed
