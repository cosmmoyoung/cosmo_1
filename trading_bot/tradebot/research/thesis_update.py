"""Stage 6: keep theses alive. New evidence -> pillar and kill-criteria check -> new conviction.

The LLM only *assesses* the evidence. What happens next (conviction math, exits,
status changes) is decided here in plain code, so behaviour is predictable.
"""

from __future__ import annotations

from datetime import datetime

from tradebot.config import ResearchConfig
from tradebot.llm import LLMRouter
from tradebot.models import NewsItem, Thesis, ThesisAssessment, ThesisDraft, ThesisEvent, clamp, iso
from tradebot.research.prompts import THESIS_UPDATE_SYSTEM

MAX_DOWN, MAX_UP = -60, 15  # one batch of news can cut conviction a lot, but raise it only a little


def is_tradeable(thesis: ThesisDraft, research: ResearchConfig, long_only: bool = True) -> bool:
    direction_ok = thesis.direction == "long" or (thesis.direction == "short" and not long_only)
    return (
        direction_ok
        and thesis.reviewer_verdict in research.allowed_verdicts
        and thesis.conviction >= research.open_conviction
    )


def render_checklist(thesis: Thesis) -> str:
    lines = [
        f"# Thesis: {thesis.ticker} ({thesis.company}), {thesis.direction}, conviction {thesis.conviction}/100",
        thesis.summary,
        "## Pillars",
        *(f"{i}. [{p.status}] {p.claim}" for i, p in enumerate(thesis.pillars)),
        "## Kill criteria",
        *(f"{i}. {k}" for i, k in enumerate(thesis.kill_criteria)),
        "## Catalysts",
        *(f"- {c}" for c in thesis.catalysts),
    ]
    return "\n".join(lines)


def assess_thesis(router: LLMRouter, thesis: Thesis, news: list[NewsItem]) -> ThesisAssessment:
    evidence = "\n\n".join(
        f"[{n.id}] {n.published_at} ({n.source}) {n.title}\n{n.summary[:1500]}\n{n.url}" for n in news
    )
    prompt = f"{render_checklist(thesis)}\n\n# New evidence\n{evidence}"
    return router.structured("thesis", THESIS_UPDATE_SYSTEM, prompt, ThesisAssessment)


def apply_assessment(thesis: Thesis, assessment: ThesisAssessment, trigger: str,
                     research: ResearchConfig, now: datetime, long_only: bool = True) -> Thesis:
    updated = thesis.model_copy(deep=True)
    before = updated.conviction
    for change in assessment.pillar_updates:
        if 0 <= change.index < len(updated.pillars):
            updated.pillars[change.index].status = change.status
    hits = sorted({i for i in assessment.kill_criteria_hit if 0 <= i < len(updated.kill_criteria)})
    note = assessment.note
    if hits:
        after = 0
        note = "触发退出条件：" + "；".join(updated.kill_criteria[i] for i in hits) + "。" + note
    else:
        after = int(clamp(before + clamp(assessment.conviction_delta, MAX_DOWN, MAX_UP), 0, 100))
    broken = sum(p.status == "broken" for p in updated.pillars)
    if broken >= research.exit_on_broken_pillars:
        after = min(after, research.exit_conviction - 1)
        note = f"{broken} 个核心假设已被证伪。" + note
    updated.conviction = after
    if updated.status == "active" and after < research.exit_conviction:
        updated.status = "closed"
    elif updated.status == "watch" and is_tradeable(updated, research, long_only):
        updated.status = "active"
    updated.history.append(ThesisEvent(
        at=iso(now), trigger=trigger, note=note, conviction_before=before, conviction_after=after,
    ))
    updated.updated_at = iso(now)
    return updated
