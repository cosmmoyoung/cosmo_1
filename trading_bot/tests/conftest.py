from __future__ import annotations

from pathlib import Path

import pytest

from tradebot.config import Settings
from tradebot.models import (
    AccountSnapshot,
    OrderProposal,
    Pillar,
    Position,
    Quote,
    Thesis,
    iso,
    utcnow,
)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    s = Settings()
    s.base_dir = tmp_path
    s.sources.fmp_news = False
    return s


def make_thesis(**overrides) -> Thesis:
    now = iso(utcnow())
    fields = dict(
        id="th-1", ticker="ABC", company="ABC Corp", industry="Semiconductors", direction="long",
        summary="ABC summary", conviction=80, reviewer_verdict="PASS", status="active",
        pillars=[Pillar(claim=f"pillar {i}", evidence="e", status="intact") for i in range(3)],
        kill_criteria=["customer leaves", "margin below 40% twice"], catalysts=[], key_risks=[],
        fair_value=120.0, max_entry_price=110.0, evidence_doc_ids=[], created_at=now, updated_at=now,
    )
    fields.update(overrides)
    return Thesis(**fields)


def make_account(cash: float = 1_000_000.0, positions: dict[str, tuple[float, float]] | None = None,
                 day_pnl_pct: float | None = 0.0) -> AccountSnapshot:
    pos = {t: Position(ticker=t, qty=q, avg_cost=p, market_price=p) for t, (q, p) in (positions or {}).items()}
    nav = cash + sum(p.value for p in pos.values())
    return AccountSnapshot(nav=nav, cash=cash, positions=pos, day_pnl_pct=day_pnl_pct)


def make_order(side: str = "BUY", quantity: int = 100, price: float = 100.0, ticker: str = "ABC") -> OrderProposal:
    now = iso(utcnow())
    return OrderProposal(id="o-1", ticker=ticker, side=side, quantity=quantity, limit_price=price,
                         reason="test", thesis_id="th-1", created_at=now, updated_at=now)


def make_quote(price: float = 100.0, market_cap: float = 50e9, ticker: str = "ABC") -> Quote:
    return Quote(ticker=ticker, price=price, market_cap=market_cap)
