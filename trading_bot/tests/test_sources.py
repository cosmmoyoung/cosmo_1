from datetime import datetime, timezone

from tradebot.sources.fmp import FMPNewsSource, parse_fmp_time


class FakeFMP:
    def __init__(self):
        self.screener_calls = 0

    def screener(self, **filters):
        self.screener_calls += 1
        return [{"symbol": "TSM", "exchangeShortName": "NYSE"}, {"symbol": "SAP", "exchangeShortName": "XETRA"}]

    def latest_stock_news(self, limit=100):
        return [
            {"symbol": "TSM", "publishedDate": "2026-09-24 13:14:38", "publisher": "Reuters",
             "title": "TSMC raises capex", "text": "...", "url": "https://example.com/tsm"},
            {"symbol": "TINY", "publishedDate": "2026-09-24 13:15:00", "publisher": "PR",
             "title": "Micro-cap pumps itself", "text": "...", "url": "https://example.com/tiny"},
            {"symbol": "TSM", "publishedDate": "2026-09-20 09:00:00", "publisher": "old",
             "title": "Old news", "text": "...", "url": "https://example.com/old"},
        ]

    def latest_press_releases(self, limit=50):
        return [{"symbol": "ASML", "publishedDate": "2026-09-24 14:00:00", "title": "ASML order intake",
                 "text": "...", "url": "https://example.com/asml"}]

    def stock_news(self, symbols, limit=50):
        return []


def test_fmp_times_are_eastern():
    assert parse_fmp_time("2026-09-24 13:14:38") == datetime(2026, 9, 24, 17, 14, 38, tzinfo=timezone.utc)


def test_news_prefilter_keeps_universe_and_watchlist():
    fmp = FakeFMP()
    source = FMPNewsSource(fmp, watchlist=["ASML"], min_market_cap=2e9)
    items = source.fetch(datetime(2026, 9, 24, tzinfo=timezone.utc))
    assert sorted(i.title for i in items) == ["ASML order intake", "TSMC raises capex"]
    source.fetch(datetime(2026, 9, 24, tzinfo=timezone.utc))
    assert fmp.screener_calls == 1  # the universe list is refreshed once a day
