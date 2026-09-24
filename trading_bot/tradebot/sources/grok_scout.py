"""Grok as a news scout: scans X and the web for market-moving items on your names and themes."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from pydantic import BaseModel, Field

from tradebot.llm import LLMRouter
from tradebot.models import NewsItem, iso, stable_id

SCOUT_SYSTEM = """You are the news scout for a fundamental, thesis-driven equity fund.
Search X and the web for new, market-relevant information: earnings and guidance,
orders and customer wins or losses, supply-chain and capacity news, regulation and
export controls, management changes, and credible expert commentary. Ignore price
chatter, memes and recycled old news. Every finding must include a source link."""


class ScoutFinding(BaseModel):
    headline: str
    summary: str
    tickers: list[str] = Field(description="US tickers the finding is about")
    url: str
    posted_at: str = Field(description="ISO date-time if known, else empty string")


class ScoutReport(BaseModel):
    findings: list[ScoutFinding]


class GrokScoutSource:
    name = "grok"

    def __init__(self, router: LLMRouter, watchlist: list[str], themes: list[str],
                 open_tickers: Callable[[], list[str]]):
        self.router = router
        self.watchlist = watchlist
        self.themes = themes
        self.open_tickers = open_tickers  # () -> tickers with an open thesis

    def fetch(self, since: datetime) -> list[NewsItem]:
        tickers = sorted({*self.watchlist, *self.open_tickers()})
        if not tickers and not self.themes:
            return []
        prompt = (
            f"Find items published since {iso(since)} (UTC).\n"
            f"Tickers to cover: {', '.join(tickers) or 'none'}\n"
            f"Themes to cover: {'; '.join(self.themes) or 'none'}\n"
            "Return at most 15 findings, most important first. Skip anything without a link."
        )
        report = self.router.structured("scout", SCOUT_SYSTEM, prompt, ScoutReport, search=True, search_since=iso(since))
        return [
            NewsItem(
                id=stable_id("grok", f.url or f.headline),
                source="grok",
                title=f.headline,
                summary=f.summary,
                url=f.url,
                tickers=[t.upper() for t in f.tickers],
                published_at=f.posted_at,
            )
            for f in report.findings
            if f.url
        ]
