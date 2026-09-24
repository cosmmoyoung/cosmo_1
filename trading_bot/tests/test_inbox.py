import json
from datetime import datetime, timezone

from tradebot.sources.inbox import InboxSource
from tradebot.store import Store


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_inbox_metadata_and_compliance_defaults(tmp_path):
    root = tmp_path / "inbox"
    write(root / "research_reports" / "ms_tsm.md",
          "---\ntickers: [TSM]\nsource: Morgan Stanley\ndate: 2026-09-20\n---\nN2 ramp ahead of plan.")
    write(root / "expert_calls" / "former_employee.md", "---\ntickers: TSM, ASML\n---\nCall notes.")
    write(root / "expert_calls" / "cleared" / "platform_call.md", "Vetted transcript about CoWoS capacity.")
    write(root / "signals" / "grok.json", json.dumps({"title": "X chatter", "text": "HBM4 pricing up", "tickers": ["MU"]}))

    store = Store(":memory:")
    inbox = InboxSource(root, store)
    items = inbox.fetch(datetime(2026, 1, 1, tzinfo=timezone.utc))
    docs = {store.get_document(i.doc_id).title: store.get_document(i.doc_id) for i in items}

    report = docs["ms tsm"]
    assert report.kind == "research_report" and report.tickers == ["TSM"] and report.source == "Morgan Stanley"
    assert report.compliance_cleared
    assert report.published_at == "2026-09-20"

    assert docs["former employee"].compliance_cleared is False  # expert calls are uncleared by default
    assert docs["former employee"].tickers == ["ASML", "TSM"]
    assert docs["platform call"].compliance_cleared is True  # the cleared/ folder
    assert docs["X chatter"].kind == "signal" and docs["X chatter"].tickers == ["MU"]

    assert "N2 ramp" in inbox.load_text(report)
    assert store.documents_for("TSM")


def test_inbox_is_stable_across_polls(tmp_path):
    root = tmp_path / "inbox"
    write(root / "research_reports" / "note.txt", "hello")
    store = Store(":memory:")
    inbox = InboxSource(root, store)
    since = datetime(2026, 1, 1, tzinfo=timezone.utc)
    first = inbox.fetch(since)
    second = inbox.fetch(since)
    assert [i.id for i in first] == [i.id for i in second]  # same id, so the bot's dedupe drops it
