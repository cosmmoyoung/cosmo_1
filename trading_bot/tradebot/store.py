"""SQLite persistence: news, documents, idea queue, theses, orders, paper account, audit log."""

from __future__ import annotations

import json
import sqlite3
from datetime import timedelta
from pathlib import Path

from tradebot.models import (
    Document,
    IndustryScan,
    NewsItem,
    OrderProposal,
    Thesis,
    TriageResult,
    iso,
    parse_iso,
    utcnow,
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY, at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS news (
    id TEXT PRIMARY KEY, source TEXT, title TEXT, url TEXT, tickers TEXT, published_at TEXT,
    materiality INTEGER, route TEXT, summary TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, tickers TEXT, payload TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS ideas (
    ticker TEXT PRIMARY KEY, reason TEXT, source TEXT, priority INTEGER, status TEXT,
    created_at TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS theses (ticker TEXT PRIMARY KEY, status TEXT, conviction INTEGER, payload TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS industry_scans (day TEXT PRIMARY KEY, payload TEXT);
CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, ticker TEXT, status TEXT, payload TEXT, created_at TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS paper_positions (ticker TEXT PRIMARY KEY, qty REAL, avg_cost REAL);
CREATE TABLE IF NOT EXISTS counters (day TEXT, name TEXT, n INTEGER, PRIMARY KEY (day, name));
CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, kind TEXT, message TEXT);
"""

OPEN_ORDER_STATUSES = ("pending_approval", "submitted")
RESEARCH_COOLDOWN_DAYS = 7


class Store:
    def __init__(self, path: Path | str):
        if str(path) != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def _exec(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def _all(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, params).fetchall()

    def _one(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, params).fetchone()

    # ---------------------------------------------------------------- meta / log
    def get_meta(self, key: str, default: str | None = None) -> str | None:
        row = self._one("SELECT value FROM meta WHERE key = ?", (key,))
        return row["value"] if row else default

    def set_meta(self, key: str, value: str) -> None:
        self._exec("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))

    def log(self, kind: str, message: str) -> None:
        self._exec("INSERT INTO events (at, kind, message) VALUES (?, ?, ?)", (iso(utcnow()), kind, message))

    def events(self, limit: int = 50) -> list[sqlite3.Row]:
        return self._all("SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))

    # ---------------------------------------------------------------- dedupe
    def is_seen(self, item_id: str) -> bool:
        return self._one("SELECT 1 FROM seen WHERE id = ?", (item_id,)) is not None

    def mark_seen(self, item_id: str) -> None:
        self._exec("INSERT OR IGNORE INTO seen (id, at) VALUES (?, ?)", (item_id, iso(utcnow())))

    # ---------------------------------------------------------------- news
    def save_news(self, item: NewsItem, triage: TriageResult | None) -> None:
        self._exec(
            "INSERT OR REPLACE INTO news VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                item.id, item.source, item.title, item.url,
                json.dumps(triage.tickers if triage and triage.tickers else item.tickers),
                item.published_at,
                triage.materiality if triage else None,
                triage.route if triage else None,
                triage.summary if triage else item.summary[:500],
                iso(utcnow()),
            ),
        )

    def recent_news(self, ticker: str | None = None, days: int = 7, min_materiality: int = 0) -> list[sqlite3.Row]:
        since = iso(utcnow() - timedelta(days=days))
        sql = "SELECT * FROM news WHERE created_at >= ? AND COALESCE(materiality, 0) >= ?"
        params: list = [since, min_materiality]
        if ticker:
            sql += " AND tickers LIKE ?"
            params.append(f'%"{ticker}"%')
        return self._all(sql + " ORDER BY created_at DESC", tuple(params))

    # ---------------------------------------------------------------- documents
    def save_document(self, doc: Document) -> None:
        self._exec(
            "INSERT OR REPLACE INTO documents VALUES (?, ?, ?, ?)",
            (doc.id, json.dumps(doc.tickers), doc.model_dump_json(), iso(utcnow())),
        )

    def get_document(self, doc_id: str) -> Document | None:
        row = self._one("SELECT payload FROM documents WHERE id = ?", (doc_id,))
        return Document.model_validate_json(row["payload"]) if row else None

    def add_document_tickers(self, doc_id: str, tickers: list[str]) -> None:
        doc = self.get_document(doc_id)
        if doc is None:
            return
        doc.tickers = sorted({*doc.tickers, *(t.upper() for t in tickers)})
        self.save_document(doc)

    def documents_for(self, ticker: str) -> list[Document]:
        rows = self._all(
            "SELECT payload FROM documents WHERE tickers LIKE ? ORDER BY created_at DESC",
            (f'%"{ticker}"%',),
        )
        return [Document.model_validate_json(r["payload"]) for r in rows]

    # ---------------------------------------------------------------- idea queue
    def enqueue_idea(self, ticker: str, reason: str, source: str, priority: int, force: bool = False) -> bool:
        """Queue a ticker for a deep dive. Returns True if it was queued or re-prioritised."""
        now = utcnow()
        row = self._one("SELECT * FROM ideas WHERE ticker = ?", (ticker,))
        if row is None:
            self._exec(
                "INSERT INTO ideas VALUES (?, ?, ?, ?, 'queued', ?, ?)",
                (ticker, reason, source, priority, iso(now), iso(now)),
            )
            return True
        if row["status"] == "queued":
            if priority > row["priority"]:
                self._exec(
                    "UPDATE ideas SET priority = ?, reason = ?, source = ?, updated_at = ? WHERE ticker = ?",
                    (priority, reason, source, iso(now), ticker),
                )
                return True
            return False
        if row["status"] == "researching":
            return False
        last = parse_iso(row["updated_at"])
        if force or last is None or now - last > timedelta(days=RESEARCH_COOLDOWN_DAYS):
            self._exec(
                "UPDATE ideas SET status = 'queued', priority = ?, reason = ?, source = ?, updated_at = ? WHERE ticker = ?",
                (priority, reason, source, iso(now), ticker),
            )
            return True
        return False

    def next_idea(self) -> sqlite3.Row | None:
        return self._one("SELECT * FROM ideas WHERE status = 'queued' ORDER BY priority DESC, created_at ASC LIMIT 1")

    def set_idea_status(self, ticker: str, status: str) -> None:
        self._exec("UPDATE ideas SET status = ?, updated_at = ? WHERE ticker = ?", (status, iso(utcnow()), ticker))

    def ideas(self, status: str | None = None) -> list[sqlite3.Row]:
        if status:
            return self._all("SELECT * FROM ideas WHERE status = ? ORDER BY priority DESC", (status,))
        return self._all("SELECT * FROM ideas ORDER BY updated_at DESC")

    # ---------------------------------------------------------------- theses
    def upsert_thesis(self, thesis: Thesis) -> None:
        self._exec(
            "INSERT OR REPLACE INTO theses VALUES (?, ?, ?, ?, ?)",
            (thesis.ticker, thesis.status, thesis.conviction, thesis.model_dump_json(), thesis.updated_at),
        )

    def get_thesis(self, ticker: str) -> Thesis | None:
        row = self._one("SELECT payload FROM theses WHERE ticker = ?", (ticker,))
        return Thesis.model_validate_json(row["payload"]) if row else None

    def theses(self, *statuses: str) -> list[Thesis]:
        if statuses:
            marks = ",".join("?" * len(statuses))
            rows = self._all(f"SELECT payload FROM theses WHERE status IN ({marks}) ORDER BY conviction DESC", statuses)
        else:
            rows = self._all("SELECT payload FROM theses ORDER BY conviction DESC")
        return [Thesis.model_validate_json(r["payload"]) for r in rows]

    # ---------------------------------------------------------------- industry scans
    def save_industry_scan(self, day: str, scan: IndustryScan) -> None:
        self._exec("INSERT OR REPLACE INTO industry_scans VALUES (?, ?)", (day, scan.model_dump_json()))

    def latest_industry_scan(self) -> IndustryScan | None:
        row = self._one("SELECT payload FROM industry_scans ORDER BY day DESC LIMIT 1")
        return IndustryScan.model_validate_json(row["payload"]) if row else None

    # ---------------------------------------------------------------- orders
    def save_order(self, order: OrderProposal) -> None:
        self._exec(
            "INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?)",
            (order.id, order.ticker, order.status, order.model_dump_json(), order.created_at, order.updated_at),
        )

    def get_order(self, order_id: str) -> OrderProposal | None:
        row = self._one("SELECT payload FROM orders WHERE id = ? OR id LIKE ?", (order_id, f"{order_id}%"))
        return OrderProposal.model_validate_json(row["payload"]) if row else None

    def orders(self, *statuses: str, limit: int = 50) -> list[OrderProposal]:
        if statuses:
            marks = ",".join("?" * len(statuses))
            rows = self._all(
                f"SELECT payload FROM orders WHERE status IN ({marks}) ORDER BY created_at DESC LIMIT ?",
                (*statuses, limit),
            )
        else:
            rows = self._all("SELECT payload FROM orders ORDER BY created_at DESC LIMIT ?", (limit,))
        return [OrderProposal.model_validate_json(r["payload"]) for r in rows]

    def has_open_order(self, ticker: str) -> bool:
        marks = ",".join("?" * len(OPEN_ORDER_STATUSES))
        row = self._one(
            f"SELECT 1 FROM orders WHERE ticker = ? AND status IN ({marks})", (ticker, *OPEN_ORDER_STATUSES)
        )
        return row is not None

    # ---------------------------------------------------------------- paper account
    def paper_cash(self, starting_cash: float) -> float:
        value = self.get_meta("paper_cash")
        if value is None:
            self.set_meta("paper_cash", str(starting_cash))
            return starting_cash
        return float(value)

    def set_paper_cash(self, cash: float) -> None:
        self.set_meta("paper_cash", repr(cash))

    def paper_positions(self) -> dict[str, tuple[float, float]]:
        return {r["ticker"]: (r["qty"], r["avg_cost"]) for r in self._all("SELECT * FROM paper_positions")}

    def set_paper_position(self, ticker: str, qty: float, avg_cost: float) -> None:
        if abs(qty) < 1e-9:
            self._exec("DELETE FROM paper_positions WHERE ticker = ?", (ticker,))
        else:
            self._exec("INSERT OR REPLACE INTO paper_positions VALUES (?, ?, ?)", (ticker, qty, avg_cost))

    # ---------------------------------------------------------------- daily counters
    def bump(self, name: str, day: str) -> int:
        self._exec(
            "INSERT INTO counters VALUES (?, ?, 1) ON CONFLICT(day, name) DO UPDATE SET n = n + 1",
            (day, name),
        )
        return self.count(name, day)

    def count(self, name: str, day: str) -> int:
        row = self._one("SELECT n FROM counters WHERE day = ? AND name = ?", (day, name))
        return row["n"] if row else 0
