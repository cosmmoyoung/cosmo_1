"""Position sizing: conviction -> target weight -> order proposal.

Conviction maps linearly to a target weight: exit_conviction (50) -> 0%,
full_conviction (95) -> max_position_pct (8%). With the defaults, 70 -> 3.6%,
80 -> 5.3%, 90 -> 7.1%. A falling conviction therefore trims automatically, and
anything below exit_conviction sells everything.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import Callable

from tradebot.config import Settings
from tradebot.models import AccountSnapshot, OrderProposal, Quote, Side, Thesis, iso, stable_id


def target_weight_pct(conviction: int, settings: Settings) -> float:
    research, risk = settings.research, settings.risk
    if conviction < research.exit_conviction:
        return 0.0
    span = max(research.full_conviction - research.exit_conviction, 1)
    return round(risk.max_position_pct * min(1.0, (conviction - research.exit_conviction) / span), 2)


def limit_price(side: Side, price: float, offset_pct: float) -> float:
    factor = 1 + offset_pct / 100 if side == "BUY" else 1 - offset_pct / 100
    return round(price * factor, 2)


def plan_order(thesis: Thesis, account: AccountSnapshot, quote: Quote, settings: Settings, now: datetime,
               round_qty: Callable[[str, int], int] = lambda ticker, qty: qty) -> OrderProposal | None:
    """The order (if any) that moves the position toward the thesis' target weight."""
    held = account.qty(thesis.ticker)
    current = account.weight_pct(thesis.ticker)
    wants_position = thesis.status == "active" and thesis.direction == "long"
    target = target_weight_pct(thesis.conviction, settings) if wants_position else 0.0

    if target == 0 and held > 0:
        side: Side = "SELL"
        qty = int(held)
        last = thesis.history[-1].note if thesis.history else ""
        reason = f"清仓：thesis 状态 {thesis.status}，conviction {thesis.conviction}。{last}"
    else:
        gap = target - current
        if target == 0 or abs(gap) < settings.risk.rebalance_band_pct:
            return None
        if gap > 0:
            if held <= 0 and thesis.conviction < settings.research.open_conviction:
                return None  # enough conviction to keep a position, not to open one
            if thesis.max_entry_price is not None and quote.price > thesis.max_entry_price:
                return None  # wait for a better price
            side = "BUY"
            qty = math.floor(gap / 100 * account.nav / quote.price)
            action = "开仓" if held <= 0 else "加仓"
        else:
            side = "SELL"
            qty = min(int(held), math.floor(-gap / 100 * account.nav / quote.price))
            action = "减仓"
        reason = (f"{action}：conviction {thesis.conviction}，目标仓位 {target:.1f}%"
                  f"（当前 {current:.1f}%）。{thesis.summary[:120]}")

    qty = round_qty(thesis.ticker, qty)
    if qty <= 0:
        return None
    return OrderProposal(
        id=stable_id("order", thesis.ticker, side, iso(now)),
        ticker=thesis.ticker,
        side=side,
        quantity=qty,
        limit_price=limit_price(side, quote.price, settings.execution.limit_offset_pct),
        reason=reason,
        thesis_id=thesis.id,
        created_at=iso(now),
        updated_at=iso(now),
    )
