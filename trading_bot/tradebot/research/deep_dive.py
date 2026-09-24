"""Stage 4: deep dive. Researcher -> critic -> reviewer (one revision round) -> PM synthesis.

The three analyst personas are the repo's own .claude/agents files, so the bot
researches the same way the stock-researcher / critical-thinker /
research-reviewer agents do in Claude Code.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime

from tradebot.config import Settings
from tradebot.llm import LLMRouter
from tradebot.models import (
    Document,
    Pillar,
    Thesis,
    ThesisDraft,
    ThesisEvent,
    Verdict,
    clamp,
    iso,
    stable_id,
    utcnow,
)
from tradebot.research.prompts import SYNTHESIS_SYSTEM, load_agent
from tradebot.research.thesis_update import is_tradeable
from tradebot.sources.inbox import InboxSource
from tradebot.store import Store

log = logging.getLogger(__name__)

VERDICT_PHRASES: tuple[tuple[str, Verdict], ...] = (
    ("PASS WITH MINOR REVISIONS", "PASS_WITH_MINOR_REVISIONS"),
    ("REVISE AND RESUBMIT", "REVISE_AND_RESUBMIT"),
    ("REJECT", "REJECT"),
    ("PASS", "PASS"),
)
VERDICT_LINE = (
    "End your audit with one final line exactly in this form:\n"
    "VERDICT: <PASS | PASS WITH MINOR REVISIONS | REVISE AND RESUBMIT | REJECT>"
)


def parse_verdict(audit: str) -> Verdict | None:
    """The reviewer's final `VERDICT:` line, or None if it is missing."""
    text = audit.upper().replace("：", ":").replace("_", " ").replace("*", "")
    marker = text.rfind("VERDICT:")
    if marker == -1:
        return None
    tail = text[marker + len("VERDICT:"):].strip()
    for phrase, verdict in VERDICT_PHRASES:
        if tail.startswith(phrase):
            return verdict
    return None


class DeepDive:
    def __init__(self, router: LLMRouter, fmp, store: Store, inbox: InboxSource, settings: Settings):
        self.router = router
        self.fmp = fmp
        self.store = store
        self.inbox = inbox
        self.settings = settings
        agents_dir = settings.path(settings.research.agents_dir)
        self.researcher = load_agent(agents_dir, "stock-researcher")
        self.critic = load_agent(agents_dir, "critical-thinker")
        self.reviewer = load_agent(agents_dir, "research-reviewer")

    # ------------------------------------------------------------------ context
    def _documents(self, ticker: str) -> list[tuple[Document, str]]:
        cfg = self.settings.research
        docs = self.store.documents_for(ticker)
        if self.settings.risk.require_compliance_cleared:
            # MNPI guard: uncleared expert-call notes never reach the analysts.
            docs = [d for d in docs if d.compliance_cleared]
        loaded = []
        for doc in docs[:cfg.max_docs]:
            text = self.inbox.load_text(doc)
            if len(text) > cfg.max_doc_chars:
                log.warning("document %s is %d chars; sending the first %d", doc.id, len(text), cfg.max_doc_chars)
                text = text[:cfg.max_doc_chars] + f"\n[... {len(text) - cfg.max_doc_chars} more characters not included ...]"
            loaded.append((doc, text))
        return loaded

    def _context(self, ticker: str, reason: str, snapshot: dict, docs: list[tuple[Document, str]]) -> str:
        parts = [
            f"<why_flagged>{reason}</why_flagged>",
            '<data_pack source="Financial Modeling Prep">\n'
            + json.dumps(snapshot, ensure_ascii=False, default=str) + "\n</data_pack>",
        ]
        news = self.store.recent_news(ticker, days=30, min_materiality=4)
        if news:
            parts.append("<recent_news>\n" + "\n".join(
                f"- {row['published_at'][:10]} [{row['source']}] {row['title']}: {row['summary']} {row['url']}"
                for row in news[:40]
            ) + "\n</recent_news>")
        if docs:
            parts.append("<documents>\n" + "\n\n".join(
                f'<document id="{doc.id}" kind="{doc.kind}" source="{doc.source}" '
                f'date="{doc.published_at}" title="{doc.title}">\n{text}\n</document>'
                for doc, text in docs
            ) + "\n</documents>")
        return "\n\n".join(parts)

    # ------------------------------------------------------------------ run
    def run(self, ticker: str, reason: str) -> Thesis:
        now = utcnow()
        snapshot = self.fmp.company_snapshot(ticker)
        docs = self._documents(ticker)
        context = self._context(ticker, reason, snapshot, docs)
        cite_rule = (
            "Cite our feeds as (Source: Financial Modeling Prep, <field>, <as_of>) or "
            "(Source: document <id>). Use web_search and web_fetch for filings, transcripts and anything missing."
        )

        memo = self.router.text("research", self.researcher, (
            f"Research {ticker} as a possible position. Work through your full framework.\n{cite_rule}\n\n{context}"
        ), search=True)
        critique = self.router.text("research", self.critic, (
            f"Stress-test the analyst's thesis on {ticker}. Your falsification criteria become the "
            f"fund's exit triggers, so make each one observable in future data.\n\n"
            f"<analyst_memo>\n{memo}\n</analyst_memo>\n\n{context}"
        ), search=True)
        audit = self._audit(ticker, memo, critique, context)
        verdict = parse_verdict(audit)
        for _ in range(self.settings.research.max_revision_rounds):
            if verdict != "REVISE_AND_RESUBMIT":
                break
            memo = self.router.text("research", self.researcher, (
                f"The quality reviewer sent your memo on {ticker} back. Address every RED and YELLOW "
                f"revision request, re-source or remove unsupported claims, and return the complete "
                f"revised memo.\n{cite_rule}\n\n<your_memo>\n{memo}\n</your_memo>\n\n"
                f"<audit>\n{audit}\n</audit>\n\n{context}"
            ), search=True)
            audit = self._audit(ticker, memo, critique, context)
            verdict = parse_verdict(audit)

        quote = snapshot.get("quote") if isinstance(snapshot.get("quote"), dict) else {}
        doc_ids = [doc.id for doc, _ in docs]
        draft = self.router.structured("thesis", SYNTHESIS_SYSTEM, (
            f"Ticker: {ticker}. Current price: {quote.get('price', 'unknown')} USD "
            f"(Financial Modeling Prep quote, {snapshot.get('as_of', '')}).\n"
            f"Document ids provided to the analysts: {', '.join(doc_ids) or 'none'}.\n\n"
            f"<analyst_memo>\n{memo}\n</analyst_memo>\n\n<critique>\n{critique}\n</critique>\n\n"
            f"<audit>\n{audit}\n</audit>"
        ), ThesisDraft)

        draft.ticker = ticker
        draft.conviction = int(clamp(draft.conviction, 0, 100))
        if verdict is None:
            # No machine-readable verdict: treat the research as not approved rather than
            # trusting the synthesizer's copy of it.
            log.warning("reviewer gave no VERDICT line for %s; treating as REVISE_AND_RESUBMIT", ticker)
        draft.reviewer_verdict = verdict or "REVISE_AND_RESUBMIT"
        draft.evidence_doc_ids = [d for d in draft.evidence_doc_ids if d in doc_ids]
        draft.pillars = [Pillar(claim=p.claim, evidence=p.evidence, status="intact") for p in draft.pillars]

        paths = self._save_memos(ticker, now, {"1_research": memo, "2_critique": critique, "3_audit": audit})
        thesis = self._to_thesis(draft, now, paths)
        self.store.upsert_thesis(thesis)
        return thesis

    def _audit(self, ticker: str, memo: str, critique: str, context: str) -> str:
        return self.router.text("research", self.reviewer, (
            f"Audit the research on {ticker} below: the analyst memo and the contrarian critique. "
            f"Verify numbers against the data pack and documents, and check sources on the web where "
            f"needed.\n\n<analyst_memo>\n{memo}\n</analyst_memo>\n\n<critique>\n{critique}\n</critique>"
            f"\n\n{context}\n\n{VERDICT_LINE}"
        ), search=True)

    def _save_memos(self, ticker: str, now: datetime, memos: dict[str, str]) -> list[str]:
        folder = self.settings.path(self.settings.research.notes_dir) / ticker
        folder.mkdir(parents=True, exist_ok=True)
        stamp = now.strftime("%Y-%m-%d_%H%M")
        paths = []
        for name, text in memos.items():
            path = folder / f"{stamp}_{name}.md"
            path.write_text(text, encoding="utf-8")
            paths.append(str(path))
        return paths

    def _to_thesis(self, draft: ThesisDraft, now: datetime, memo_paths: list[str]) -> Thesis:
        previous = self.store.get_thesis(draft.ticker)
        status = "active" if is_tradeable(draft, self.settings.research, self.settings.risk.long_only) else "watch"
        thesis = Thesis(
            **draft.model_dump(),
            id=previous.id if previous else stable_id("thesis", draft.ticker, iso(now)),
            status=status,
            created_at=previous.created_at if previous else iso(now),
            updated_at=iso(now),
            history=list(previous.history) if previous else [],
            memo_paths=memo_paths,
        )
        thesis.history.append(ThesisEvent(
            at=iso(now),
            trigger="deep_dive",
            note=f"完成深度研究，审核结论 {thesis.reviewer_verdict}，状态 {status}",
            conviction_before=previous.conviction if previous else 0,
            conviction_after=thesis.conviction,
        ))
        return thesis
