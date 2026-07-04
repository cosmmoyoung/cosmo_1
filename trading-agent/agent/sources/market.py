"""行情数据采集。

优先级:FMP(填了 key)> Yahoo Finance 免费接口 > 本地 fixture(demo 模式)。
统一输出格式,下游不关心数据从哪来:
    {symbol, name, price, change_pct, volume, year_high, year_low,
     avg50, avg200, theme}
"""
import json
import time
from pathlib import Path

import requests

FIXTURE = Path(__file__).resolve().parent.parent.parent / "data" / "fixtures" / "market.json"

UA = {"User-Agent": "Mozilla/5.0 (market-monitor-agent; personal research use)"}


def fetch_market(cfg: dict, demo: bool = False) -> list[dict]:
    themes = {w["symbol"]: w.get("theme", "") for w in cfg["watchlist"]}
    symbols = list(themes)

    if demo:
        rows = json.loads(FIXTURE.read_text(encoding="utf-8"))
    elif cfg["env"]["fmp_key"]:
        rows = _fetch_fmp(symbols, cfg["env"]["fmp_key"])
    else:
        rows = _fetch_yahoo(symbols)

    for r in rows:
        r["theme"] = themes.get(r["symbol"], "")
    return rows


def _fetch_fmp(symbols: list[str], key: str) -> list[dict]:
    url = "https://financialmodelingprep.com/stable/batch-quote"
    resp = requests.get(url, params={"symbols": ",".join(symbols), "apikey": key},
                        timeout=30, headers=UA)
    resp.raise_for_status()
    return [
        {
            "symbol": q["symbol"], "name": q.get("name", q["symbol"]),
            "price": q["price"], "change_pct": q.get("changePercentage", 0.0),
            "volume": q.get("volume", 0),
            "year_high": q.get("yearHigh"), "year_low": q.get("yearLow"),
            "avg50": q.get("priceAvg50"), "avg200": q.get("priceAvg200"),
        }
        for q in resp.json()
    ]


def _fetch_yahoo(symbols: list[str]) -> list[dict]:
    """Yahoo 的公开 chart 接口,不需要 key。逐个请求,礼貌限速。"""
    rows = []
    for sym in symbols:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
        resp = requests.get(url, params={"range": "1y", "interval": "1d"},
                            timeout=30, headers=UA)
        resp.raise_for_status()
        result = resp.json()["chart"]["result"][0]
        meta = result["meta"]
        closes = [c for c in result["indicators"]["quote"][0]["close"] if c is not None]
        price = meta["regularMarketPrice"]
        prev = meta.get("chartPreviousClose") or (closes[-2] if len(closes) > 1 else price)
        rows.append({
            "symbol": sym, "name": meta.get("longName", sym),
            "price": price,
            "change_pct": (price - prev) / prev * 100 if prev else 0.0,
            "volume": meta.get("regularMarketVolume", 0),
            "year_high": max(closes) if closes else None,
            "year_low": min(closes) if closes else None,
            "avg50": sum(closes[-50:]) / min(50, len(closes)) if closes else None,
            "avg200": sum(closes[-200:]) / min(200, len(closes)) if closes else None,
        })
        time.sleep(0.5)
    return rows
