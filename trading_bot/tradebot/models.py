"""Domain objects and the structured outputs the LLM stages must return.

LLM output models are kept flat and constraint-free so they work with
structured outputs; numeric ranges (0-100 conviction, 0-10 materiality) are
stated in field descriptions and enforced in code, never trusted.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat(timespec="seconds")


def parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def stable_id(*parts: object) -> str:
    return hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:16]


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


# --------------------------------------------------------------------------- inputs

class NewsItem(BaseModel):
    id: str
    source: str
    title: str
    summary: str = ""
    url: str = ""
    tickers: list[str] = Field(default_factory=list)
    published_at: str = ""
    doc_id: str | None = None  # set when the item comes from an inbox document


DocKind = Literal["research_report", "expert_call", "signal"]


class Document(BaseModel):
    """A research report, expert-call note or external signal dropped into the inbox."""

    id: str
    kind: DocKind
    title: str
    path: str
    source: str = ""
    tickers: list[str] = Field(default_factory=list)
    published_at: str = ""
    compliance_cleared: bool = True
    summary: str = ""


class Quote(BaseModel):
    ticker: str
    price: float
    market_cap: float | None = None


# ------------------------------------------------------------------ LLM stage outputs

Route = Literal["ignore", "thesis_check", "new_idea", "both"]


class TriageResult(BaseModel):
    item_id: str
    materiality: int = Field(description="0-10. 0 = noise, 5 = worth logging, 8+ = could change a thesis or move the stock")
    tickers: list[str] = Field(description="US tickers the item is materially about, e.g. TSM, NVDA")
    industries: list[str]
    event_type: str = Field(description="earnings, guidance, M&A, regulation, product, supply chain, management, macro, other")
    summary: str = Field(description="One plain sentence: what happened and why it matters")
    route: Route = Field(description="thesis_check if it touches an open thesis, new_idea if it suggests a stock worth researching")


class TriageBatch(BaseModel):
    results: list[TriageResult]


class IndustryView(BaseModel):
    industry: str = Field(description="Industry name exactly as given in the input data")
    score: int = Field(description="0-100 attractiveness over the next 6-24 months")
    stance: Literal["overweight", "neutral", "underweight"]
    why: str
    drivers: list[str]
    what_would_change_view: list[str]


class IndustryScan(BaseModel):
    industries: list[IndustryView]


class CandidateView(BaseModel):
    ticker: str
    score: int = Field(description="0-100: how much a full deep dive is worth")
    why: str
    red_flags: list[str]


class CandidateRanking(BaseModel):
    candidates: list[CandidateView]


PillarStatus = Literal["intact", "weakened", "broken"]
Verdict = Literal["PASS", "PASS_WITH_MINOR_REVISIONS", "REVISE_AND_RESUBMIT", "REJECT"]
Direction = Literal["long", "short", "none"]


class Pillar(BaseModel):
    claim: str = Field(description="A load-bearing assumption stated so it can be checked later, e.g. 'HBM share stays above 50% through 2027'")
    evidence: str
    status: PillarStatus


class ThesisDraft(BaseModel):
    ticker: str
    company: str
    industry: str
    direction: Direction = Field(description="none = do not trade")
    summary: str
    pillars: list[Pillar] = Field(description="3-5 load-bearing assumptions")
    kill_criteria: list[str] = Field(description="Observable events that prove the thesis wrong; any single one means exit")
    catalysts: list[str]
    key_risks: list[str]
    fair_value: float | None = Field(description="Per-share fair value in USD; null if it cannot be estimated")
    max_entry_price: float | None = Field(description="Do not buy above this USD price; null if it cannot be estimated")
    conviction: int = Field(description="0-100, calibrated: 50 = coin flip, 70 = starter position, 85 = high, 90+ = rare")
    reviewer_verdict: Verdict
    evidence_doc_ids: list[str] = Field(description="ids of the provided documents the thesis relies on")


class ThesisEvent(BaseModel):
    at: str
    trigger: str
    note: str
    conviction_before: int
    conviction_after: int


class Thesis(ThesisDraft):
    id: str
    status: Literal["watch", "active", "closed"] = "watch"
    created_at: str
    updated_at: str
    history: list[ThesisEvent] = Field(default_factory=list)
    memo_paths: list[str] = Field(default_factory=list)


class PillarUpdate(BaseModel):
    index: int = Field(description="0-based index of the pillar")
    status: PillarStatus
    reason: str


class ThesisAssessment(BaseModel):
    pillar_updates: list[PillarUpdate]
    kill_criteria_hit: list[int] = Field(description="0-based indexes of kill criteria the new evidence clearly meets; usually empty")
    conviction_delta: int = Field(description="Routine news -3..+3; material news -15..+10; thesis-breaking news -30 or lower")
    note: str = Field(description="What changed and why, in two or three plain sentences")
    needs_full_refresh: bool = Field(description="True only if the news is big enough to redo the full deep dive")


# ----------------------------------------------------------------- account & orders

class Position(BaseModel):
    ticker: str
    qty: float
    avg_cost: float
    market_price: float

    @property
    def value(self) -> float:
        return self.qty * self.market_price


class AccountSnapshot(BaseModel):
    nav: float
    cash: float
    positions: dict[str, Position] = Field(default_factory=dict)
    day_pnl_pct: float | None = None

    def qty(self, ticker: str) -> float:
        pos = self.positions.get(ticker)
        return pos.qty if pos else 0.0

    def value(self, ticker: str) -> float:
        pos = self.positions.get(ticker)
        return pos.value if pos else 0.0

    def weight_pct(self, ticker: str) -> float:
        return 100.0 * self.value(ticker) / self.nav if self.nav > 0 else 0.0

    @property
    def gross_exposure(self) -> float:
        return sum(abs(p.value) for p in self.positions.values())


Side = Literal["BUY", "SELL"]
OrderStatus = Literal[
    "pending_approval", "rejected", "submitted", "filled", "cancelled", "expired", "failed"
]


class OrderProposal(BaseModel):
    id: str
    ticker: str
    side: Side
    quantity: int
    limit_price: float
    reason: str
    thesis_id: str | None = None
    status: OrderStatus = "pending_approval"
    risk_notes: list[str] = Field(default_factory=list)
    broker_order_id: str | None = None
    filled_qty: float = 0.0
    avg_fill_price: float | None = None
    created_at: str
    updated_at: str

    @property
    def notional(self) -> float:
        return self.quantity * self.limit_price


class OrderResult(BaseModel):
    broker_order_id: str
    status: str
    filled_qty: float = 0.0
    avg_price: float | None = None
