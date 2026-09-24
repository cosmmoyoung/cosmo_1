"""Local inbox for research reports, expert-call notes and signals from other bots.

    inbox/
      research_reports/      broker research (.pdf .md .txt)
      expert_calls/          expert-call notes: NOT compliance-cleared by default
      expert_calls/cleared/  notes from platforms with a compliance review
      signals/               .json / .md dropped by other bots (e.g. your Grok bot)

Metadata goes in YAML front matter (.md/.txt) or a same-name .yaml file next to
a PDF (report.pdf + report.yaml):

    tickers: [TSM, ASML]
    source: Morgan Stanley
    date: 2026-09-20
    compliance_cleared: true

Expert-call notes can carry material non-public information (MNPI). Unless a
note is cleared, the deep dive never sees it and the risk engine blocks any
trade that cites it.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from tradebot.models import Document, NewsItem, iso, stable_id
from tradebot.store import Store

log = logging.getLogger(__name__)

KIND_DIRS = {"research_reports": "research_report", "expert_calls": "expert_call", "signals": "signal"}
DOC_SUFFIXES = {".md", ".txt", ".json", ".pdf"}
SUMMARY_CHARS = 1500


def split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            if isinstance(meta, dict):
                return meta, text[end + 4:].lstrip("\n")
    return {}, text


def _tickers(value: Any) -> list[str]:
    if isinstance(value, str):
        value = value.replace(";", ",").split(",")
    return sorted({str(t).strip().upper() for t in (value or []) if str(t).strip()})


def read_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        log.warning("pypdf is not installed; skipping %s (pip install 'tradebot[pdf]')", path.name)
        return ""
    return "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)


class InboxSource:
    name = "inbox"

    def __init__(self, root: Path, store: Store):
        self.root = root
        self.store = store

    def ensure_dirs(self) -> None:
        for sub in ("research_reports", "expert_calls/cleared", "signals"):
            (self.root / sub).mkdir(parents=True, exist_ok=True)

    def _files(self):
        for folder, kind in KIND_DIRS.items():
            base = self.root / folder
            if not base.exists():
                continue
            for path in sorted(base.rglob("*")):
                if path.is_file() and path.suffix.lower() in DOC_SUFFIXES:
                    yield kind, path

    def read(self, path: Path) -> tuple[dict[str, Any], str]:
        """Return (metadata, full text) for one inbox file."""
        if path.suffix.lower() == ".pdf":
            sidecar = path.with_suffix(".yaml")
            meta = yaml.safe_load(sidecar.read_text(encoding="utf-8")) if sidecar.exists() else {}
            return meta or {}, read_pdf(path)
        raw = path.read_text(encoding="utf-8", errors="replace")
        if path.suffix.lower() == ".json":
            data = json.loads(raw)
            data = data if isinstance(data, dict) else {"text": json.dumps(data, ensure_ascii=False)}
            return data, str(data.get("text") or data.get("summary") or "")
        return split_front_matter(raw)

    def load_text(self, doc: Document) -> str:
        return self.read(Path(doc.path))[1]

    def _document(self, kind: str, path: Path, doc_id: str) -> Document:
        meta, text = self.read(path)
        relative = path.relative_to(self.root)
        if "compliance_cleared" in meta:
            cleared = bool(meta["compliance_cleared"])
        else:
            cleared = kind != "expert_call" or "cleared" in relative.parts
        return Document(
            id=doc_id,
            kind=kind,
            title=str(meta.get("title") or path.stem.replace("_", " ")),
            path=str(path),
            source=str(meta.get("source") or ""),
            tickers=_tickers(meta.get("tickers")),
            published_at=str(meta.get("date") or ""),
            compliance_cleared=cleared,
            summary=" ".join(text.split())[:SUMMARY_CHARS],
        )

    def fetch(self, since: datetime) -> list[NewsItem]:
        """Every inbox file becomes a NewsItem; the bot's dedupe drops ones already triaged."""
        items = []
        for kind, path in self._files():
            stat = path.stat()
            doc_id = stable_id(path.relative_to(self.root), stat.st_mtime_ns, stat.st_size)
            doc = self.store.get_document(doc_id)
            if doc is None:
                try:
                    doc = self._document(kind, path, doc_id)
                except Exception as exc:  # a malformed file must not stop the whole cycle
                    log.warning("could not read %s: %s", path, exc)
                    continue
                self.store.save_document(doc)
            items.append(NewsItem(
                id=f"doc:{doc.id}",
                source=f"inbox:{doc.kind}",
                title=doc.title,
                summary=doc.summary,
                tickers=doc.tickers,
                published_at=doc.published_at or iso(datetime.fromtimestamp(stat.st_mtime).astimezone()),
                doc_id=doc.id,
            ))
        return items
