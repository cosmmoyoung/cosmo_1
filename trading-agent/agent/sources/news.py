"""新闻采集:RSS(免费)+ 可选 FMP 个股新闻。

统一输出:{source, title, summary, url, published}
"""
import json
from pathlib import Path

import requests

FIXTURE = Path(__file__).resolve().parent.parent.parent / "data" / "fixtures" / "news.json"


def fetch_news(cfg: dict, demo: bool = False, max_per_feed: int = 10) -> list[dict]:
    if demo:
        return json.loads(FIXTURE.read_text(encoding="utf-8"))

    items: list[dict] = []
    items += _fetch_rss(cfg.get("rss_feeds", []), max_per_feed)
    if cfg["env"]["fmp_key"]:
        items += _fetch_fmp_news(cfg)
    return items


def _fetch_rss(feeds: list[dict], max_per_feed: int) -> list[dict]:
    import feedparser  # 延迟导入,demo 模式不需要装它

    items = []
    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:max_per_feed]:
                items.append({
                    "source": feed["name"],
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", "")[:500],
                    "url": entry.get("link", ""),
                    "published": entry.get("published", ""),
                })
        except Exception as e:  # 单个源挂了不影响整体
            print(f"[warn] RSS 源 {feed['name']} 抓取失败: {e}")
    return items


def _fetch_fmp_news(cfg: dict, limit: int = 30) -> list[dict]:
    symbols = ",".join(w["symbol"] for w in cfg["watchlist"])
    resp = requests.get(
        "https://financialmodelingprep.com/stable/news/stock",
        params={"symbols": symbols, "limit": limit, "apikey": cfg["env"]["fmp_key"]},
        timeout=30,
    )
    resp.raise_for_status()
    return [
        {
            "source": a.get("publisher", "FMP"),
            "title": a.get("title", ""),
            "summary": a.get("text", "")[:500],
            "url": a.get("url", ""),
            "published": a.get("publishedDate", ""),
            "symbol": a.get("symbol", ""),
        }
        for a in resp.json()
    ]
