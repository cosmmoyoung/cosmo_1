"""Stage 2: industry scan. Which industries deserve attention over the next 6-24 months?"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, timedelta

from tradebot.llm import LLMRouter
from tradebot.models import IndustryScan, Thesis
from tradebot.research.prompts import INDUSTRY_SYSTEM
from tradebot.store import Store

MOMENTUM_DAYS = 5
EXCHANGES = ("NASDAQ", "NYSE")  # FMP snapshots are per exchange


def _trading_days_back(today: date, n: int) -> list[date]:
    days, day = [], today
    while len(days) < n:
        day -= timedelta(days=1)
        if day.weekday() < 5:
            days.append(day)
    return days


def industry_inputs(fmp, today: date) -> dict[str, dict]:
    """Per industry: summed daily % change over the last few sessions, plus the latest P/E."""
    change: dict[str, float] = defaultdict(float)
    for day in _trading_days_back(today, MOMENTUM_DAYS):
        by_industry: dict[str, list[float]] = defaultdict(list)
        for exchange in EXCHANGES:
            for row in fmp.industry_performance(day, exchange) or []:
                if row.get("industry") and row.get("averageChange") is not None:
                    by_industry[row["industry"]].append(float(row["averageChange"]))
        for industry, changes in by_industry.items():
            change[industry] += sum(changes) / len(changes)
    pe: dict[str, list[float]] = defaultdict(list)
    latest = _trading_days_back(today, 1)[0]
    for exchange in EXCHANGES:
        for row in fmp.industry_pe(latest, exchange) or []:
            # FMP reports 0 or near-zero P/E when the figure is not meaningful.
            if row.get("industry") and (row.get("pe") or 0) > 1:
                pe[row["industry"]].append(float(row["pe"]))
    return {
        industry: {
            "change_5d_pct": round(value, 2),
            "pe": round(sum(pe[industry]) / len(pe[industry]), 1) if pe.get(industry) else None,
        }
        for industry, value in change.items()
    }


def scan_industries(router: LLMRouter, fmp, store: Store, themes: list[str],
                    theses: list[Thesis], today: date) -> IndustryScan:
    stats = industry_inputs(fmp, today)
    news = store.recent_news(days=7, min_materiality=6)
    headlines = [f"- {row['summary']} (tickers: {', '.join(json.loads(row['tickers']))})" for row in news[:80]]
    lines = [
        f"Date: {today.isoformat()}",
        "## Fund themes", *[f"- {t}" for t in themes],
        "## Current theses", *[f"- {t.ticker}: {t.industry}" for t in theses],
        "## Material news of the past week", *headlines,
        "## Industry data (Financial Modeling Prep): 5-session % change and P/E",
        json.dumps(stats, ensure_ascii=False),
        "",
        "Score the 15 most interesting industries.",
    ]
    scan = router.structured("industry", INDUSTRY_SYSTEM, "\n".join(lines), IndustryScan)
    if stats:
        scan.industries = [v for v in scan.industries if v.industry in stats]
    for view in scan.industries:
        view.score = max(0, min(100, view.score))
    scan.industries.sort(key=lambda v: v.score, reverse=True)
    return scan
