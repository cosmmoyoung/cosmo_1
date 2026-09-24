"""Stage 1: news triage. Cheap and fast: most items are noise and stop here."""

from __future__ import annotations

from tradebot.llm import LLMRouter
from tradebot.models import NewsItem, Thesis, TriageBatch, TriageResult
from tradebot.research.prompts import TRIAGE_SYSTEM

BATCH_SIZE = 25


def _render(items: list[NewsItem], theses: list[Thesis], themes: list[str]) -> str:
    lines = ["## Open theses"]
    lines += [f"- {t.ticker} ({t.company}): {t.summary[:200]}" for t in theses] or ["- none"]
    lines += ["", "## Fund themes", *(f"- {theme}" for theme in themes or ["none"]), "", "## Items"]
    for item in items:
        tickers = ", ".join(item.tickers) or "unknown"
        lines.append(f"[{item.id}] ({item.source}; tickers: {tickers}) {item.title}\n{item.summary[:600]}")
    return "\n".join(lines)


def triage_items(router: LLMRouter, items: list[NewsItem], theses: list[Thesis],
                 themes: list[str]) -> list[tuple[NewsItem, TriageResult]]:
    results: list[tuple[NewsItem, TriageResult]] = []
    for start in range(0, len(items), BATCH_SIZE):
        batch = items[start:start + BATCH_SIZE]
        answer = router.structured("triage", TRIAGE_SYSTEM, _render(batch, theses, themes), TriageBatch)
        by_id = {r.item_id: r for r in answer.results}
        for item in batch:
            result = by_id.get(item.id) or TriageResult(
                item_id=item.id, materiality=0, tickers=item.tickers, industries=[],
                event_type="other", summary="(not triaged)", route="ignore",
            )
            result.materiality = max(0, min(10, result.materiality))
            result.tickers = sorted({t.strip().upper() for t in result.tickers if t.strip()})
            results.append((item, result))
    return results
