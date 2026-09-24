"""Brokers. The bot only ever talks to the Broker interface, so paper and IBKR are interchangeable."""

from __future__ import annotations

from typing import Protocol

from tradebot.models import AccountSnapshot, OrderResult, Side


class Broker(Protocol):
    name: str
    is_live: bool

    def account(self) -> AccountSnapshot: ...

    def place_limit_order(self, ticker: str, side: Side, quantity: int, limit_price: float) -> OrderResult: ...

    def order_status(self, broker_order_id: str) -> OrderResult | None: ...

    def round_quantity(self, ticker: str, quantity: int) -> int: ...
