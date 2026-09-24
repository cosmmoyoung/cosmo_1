"""Where information comes from: market data/news (FMP), X and web (Grok), and the local inbox."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol

from tradebot.models import NewsItem


class NewsSource(Protocol):
    name: str

    def fetch(self, since: datetime) -> list[NewsItem]: ...
