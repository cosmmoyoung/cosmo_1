"""Financial Modeling Prep client (stable REST API) and the FMP news source.

All endpoint paths live in this file so a change on FMP's side is a one-line fix.
Note: FMP fundamentals for ADRs are reported in the issuer's currency (TSM in
TWD), while quotes are in USD; the data pack sent to the LLM keeps
`reportedCurrency` next to the numbers so the model does not mix them.
"""

from __future__ import annotations

import os
from datetime import date, datetime, timezone
from typing import Any
from zoneinfo import ZoneInfo

import requests

from tradebot.models import NewsItem, Quote, iso, stable_id

FMP_BASE = "https://financialmodelingprep.com/stable"
NEW_YORK = ZoneInfo("America/New_York")  # FMP news timestamps are US Eastern time
US_EXCHANGES = {"NASDAQ", "NYSE", "AMEX"}


class FMPError(RuntimeError):
    pass


def parse_fmp_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return (dt if dt.tzinfo else dt.replace(tzinfo=NEW_YORK)).astimezone(timezone.utc)


class FMPClient:
    def __init__(self, api_key: str | None = None, session: requests.Session | None = None, timeout: float = 30):
        self.api_key = api_key or os.environ.get("FMP_API_KEY", "")
        if not self.api_key:
            raise FMPError("FMP_API_KEY is not set")
        self.session = session or requests.Session()
        self.timeout = timeout

    def get(self, path: str, **params: Any) -> Any:
        query = {k: v for k, v in params.items() if v is not None}
        query["apikey"] = self.api_key
        resp = self.session.get(f"{FMP_BASE}/{path}", params=query, timeout=self.timeout)
        if resp.status_code != 200:
            raise FMPError(f"{path}: HTTP {resp.status_code} {resp.text[:200]}")
        data = resp.json()
        if isinstance(data, dict) and "Error Message" in data:
            raise FMPError(f"{path}: {data['Error Message']}")
        return data

    # ------------------------------------------------------------------ news
    def latest_stock_news(self, limit: int = 100) -> list[dict]:
        return self.get("news/stock-latest", page=0, limit=limit)

    def stock_news(self, symbols: list[str], limit: int = 50) -> list[dict]:
        return self.get("news/stock", symbols=",".join(symbols), limit=limit)

    def latest_press_releases(self, limit: int = 50) -> list[dict]:
        return self.get("news/press-releases-latest", page=0, limit=limit)

    # ------------------------------------------------------------------ market structure
    def industry_performance(self, day: date, exchange: str | None = None) -> list[dict]:
        return self.get("industry-performance-snapshot", date=day.isoformat(), exchange=exchange)

    def industry_pe(self, day: date, exchange: str | None = None) -> list[dict]:
        return self.get("industry-pe-snapshot", date=day.isoformat(), exchange=exchange)

    def screener(self, **filters: Any) -> list[dict]:
        return self.get("company-screener", **filters)

    # ------------------------------------------------------------------ company
    def quote(self, symbol: str) -> Quote | None:
        rows = self.get("quote", symbol=symbol)
        if not rows or rows[0].get("price") is None:
            return None
        row = rows[0]
        return Quote(ticker=symbol, price=float(row["price"]), market_cap=row.get("marketCap"))

    def key_metrics_ttm(self, symbol: str) -> dict:
        rows = self.get("key-metrics-ttm", symbol=symbol)
        return rows[0] if rows else {}

    def company_snapshot(self, symbol: str) -> dict[str, Any]:
        """Everything the deep dive needs as a data pack. Missing pieces are reported, not fatal."""
        calls = {
            "profile": ("profile", {"symbol": symbol}),
            "quote": ("quote", {"symbol": symbol}),
            "key_metrics_ttm": ("key-metrics-ttm", {"symbol": symbol}),
            "ratios_ttm": ("ratios-ttm", {"symbol": symbol}),
            "income_statements_annual": ("income-statement", {"symbol": symbol, "period": "annual", "limit": 5}),
            "cash_flow_annual": ("cash-flow-statement", {"symbol": symbol, "period": "annual", "limit": 5}),
            "price_target_consensus": ("price-target-consensus", {"symbol": symbol}),
        }
        snapshot: dict[str, Any] = {"symbol": symbol, "source": "Financial Modeling Prep", "as_of": iso(datetime.now(timezone.utc))}
        for key, (path, params) in calls.items():
            try:
                data = self.get(path, **params)
            except (FMPError, requests.RequestException) as exc:
                snapshot[key] = f"unavailable: {exc}"
                continue
            if key in ("profile", "quote", "key_metrics_ttm", "ratios_ttm", "price_target_consensus"):
                data = data[0] if isinstance(data, list) and data else data
            if key == "profile" and isinstance(data, dict) and data.get("description"):
                data["description"] = data["description"][:1500]
            snapshot[key] = data
        return snapshot


class FMPNewsSource:
    """Latest stock news and press releases, pre-filtered to companies the fund could own.

    The pre-filter (US-listed, above the minimum market cap, refreshed daily with one
    screener call) drops most micro-cap noise before it costs any LLM tokens.
    """

    name = "fmp"

    def __init__(self, client: FMPClient, watchlist: list[str] | None = None, min_market_cap: float = 0):
        self.client = client
        self.watchlist = [t.upper() for t in (watchlist or [])]
        self.min_market_cap = min_market_cap
        self._universe: set[str] | None = None
        self._universe_day: date | None = None

    def universe(self) -> set[str] | None:
        today = datetime.now(timezone.utc).date()
        if self.min_market_cap > 0 and self._universe_day != today:
            try:
                rows = self.client.screener(
                    marketCapMoreThan=int(self.min_market_cap), isActivelyTrading=True,
                    isEtf=False, isFund=False, limit=10000,
                )
                self._universe = {r["symbol"] for r in rows if r.get("exchangeShortName") in US_EXCHANGES}
                self._universe_day = today
            except (FMPError, requests.RequestException):
                self._universe = None  # no filter today rather than no news
        return self._universe

    def fetch(self, since: datetime) -> list[NewsItem]:
        rows = self.client.latest_stock_news(limit=100) + self.client.latest_press_releases(limit=50)
        if self.watchlist:
            rows += self.client.stock_news(self.watchlist[:25], limit=50)
        universe = self.universe()
        items: dict[str, NewsItem] = {}
        for row in rows:
            published = parse_fmp_time(row.get("publishedDate"))
            if published is None or published < since:
                continue
            symbol = (row.get("symbol") or "").upper()
            if universe and symbol and symbol not in universe and symbol not in self.watchlist:
                continue
            key = row.get("url") or row.get("title") or ""
            item = NewsItem(
                id=stable_id("fmp", key),
                source=f"fmp:{row.get('publisher') or row.get('site') or 'news'}",
                title=(row.get("title") or "").strip(),
                summary=(row.get("text") or "")[:1200],
                url=row.get("url") or "",
                tickers=[symbol] if symbol else [],
                published_at=iso(published),
            )
            items[item.id] = item
        return list(items.values())
