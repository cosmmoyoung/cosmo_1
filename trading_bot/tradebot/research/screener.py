"""Stage 3: company screen. Hard filters in code, judgment by the LLM."""

from __future__ import annotations

import json
import re

from tradebot.config import UniverseConfig
from tradebot.llm import LLMRouter
from tradebot.models import CandidateRanking, IndustryView
from tradebot.research.prompts import SCREEN_SYSTEM
from tradebot.sources.fmp import US_EXCHANGES

US_TICKER = re.compile(r"^[A-Z]{1,5}([.-][A-Z])?$")
MAX_TO_ENRICH = 15
METRIC_KEYS = (
    "returnOnInvestedCapitalTTM", "returnOnEquityTTM", "evToEBITDATTM", "evToSalesTTM",
    "freeCashFlowYieldTTM", "netDebtToEBITDATTM", "capexToRevenueTTM",
)


def in_universe(ticker: str, universe: UniverseConfig) -> bool:
    return bool(US_TICKER.match(ticker)) and ticker not in {t.upper() for t in universe.exclude}


def screen_industry(router: LLMRouter, fmp, view: IndustryView, universe: UniverseConfig,
                    skip: set[str]) -> CandidateRanking:
    rows = fmp.screener(
        industry=view.industry,
        marketCapMoreThan=int(universe.min_market_cap_usd),
        priceMoreThan=universe.min_price,
        isActivelyTrading=True, isEtf=False, isFund=False, limit=60,
    ) or []
    rows = [
        r for r in rows
        if r.get("exchangeShortName") in US_EXCHANGES
        and in_universe(r.get("symbol", ""), universe)
        and r["symbol"] not in skip
    ]
    rows.sort(key=lambda r: r.get("marketCap") or 0, reverse=True)
    companies = []
    for row in rows[:MAX_TO_ENRICH]:
        try:
            metrics = fmp.key_metrics_ttm(row["symbol"])
        except Exception:
            metrics = {}
        companies.append({
            "ticker": row["symbol"],
            "name": row.get("companyName"),
            "country": row.get("country"),
            "market_cap_usd": row.get("marketCap"),
            "beta": row.get("beta"),
            **{k: metrics.get(k) for k in METRIC_KEYS},
        })
    if not companies:
        return CandidateRanking(candidates=[])
    prompt = "\n".join([
        f"Industry: {view.industry} (score {view.score}, {view.stance})",
        f"Why this industry: {view.why}",
        f"Key drivers: {'; '.join(view.drivers)}",
        "",
        "Candidates with TTM metrics from Financial Modeling Prep (ratios are fractions, e.g. 0.27 = 27%;",
        "metrics are in each company's reporting currency, which can differ from USD for ADRs):",
        json.dumps(companies, ensure_ascii=False),
        "",
        "Rank the best candidates for a full deep dive (at most 5).",
    ])
    ranking = router.structured("screen", SCREEN_SYSTEM, prompt, CandidateRanking)
    allowed = {c["ticker"] for c in companies}
    ranking.candidates = sorted(
        (c for c in ranking.candidates if c.ticker.upper() in allowed),
        key=lambda c: c.score, reverse=True,
    )
    for c in ranking.candidates:
        c.ticker = c.ticker.upper()
        c.score = max(0, min(100, c.score))
    return ranking
