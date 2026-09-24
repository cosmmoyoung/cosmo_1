"""Request-shape tests for the Claude and Grok providers, using mocked HTTP (no API calls)."""

import json

import anthropic
import httpx2
import pytest

from tradebot.config import LLMTask
from tradebot.llm import LLMRefusal
from tradebot.llm.claude import ClaudeProvider
from tradebot.llm.grok import GrokProvider, extract_json
from tradebot.models import TriageBatch


def claude_client(handler) -> anthropic.Anthropic:
    return anthropic.Anthropic(
        api_key="test-key", max_retries=0,
        http_client=anthropic.DefaultHttpxClient(transport=httpx2.MockTransport(handler)),
    )


def message(content, stop_reason="end_turn"):
    return {
        "id": "msg_test", "type": "message", "role": "assistant", "model": "claude-opus-5",
        "content": content, "stop_reason": stop_reason, "stop_sequence": None,
        "usage": {"input_tokens": 10, "output_tokens": 5},
    }


TRIAGE = {"results": [{
    "item_id": "n1", "materiality": 7, "tickers": ["TSM"], "industries": ["Semiconductors"],
    "event_type": "guidance", "summary": "raised guidance", "route": "thesis_check",
}]}


def test_structured_request_shape():
    seen = {}

    def handler(request: httpx2.Request) -> httpx2.Response:
        seen["body"] = json.loads(request.content)
        seen["beta"] = request.headers.get("anthropic-beta", "")
        return httpx2.Response(200, json=message([{"type": "text", "text": json.dumps(TRIAGE)}]))

    provider = ClaudeProvider(claude_client(handler))
    result = provider.structured(LLMTask(model="claude-opus-5", effort="low"), "system", "prompt", TriageBatch)

    body = seen["body"]
    assert result.results[0].tickers == ["TSM"]
    assert body["model"] == "claude-opus-5"
    assert body["fallbacks"] == "default"
    assert "server-side-fallback-2026-07-01" in seen["beta"]
    assert body["thinking"] == {"type": "adaptive"}
    assert body["output_config"]["effort"] == "low"
    assert body["output_config"]["format"]["type"] == "json_schema"
    assert body["system"][0]["cache_control"] == {"type": "ephemeral"}


def test_haiku_gets_no_effort_or_fallbacks():
    seen = {}

    def handler(request):
        seen["body"] = json.loads(request.content)
        return httpx2.Response(200, json=message([{"type": "text", "text": json.dumps(TRIAGE)}]))

    ClaudeProvider(claude_client(handler)).structured(
        LLMTask(model="claude-haiku-4-5", effort="low"), "s", "p", TriageBatch)
    body = seen["body"]
    assert "fallbacks" not in body and "thinking" not in body and "effort" not in body.get("output_config", {})


def test_refusal_raises():
    def handler(request):
        return httpx2.Response(200, json=message([], stop_reason="refusal"))

    with pytest.raises(LLMRefusal):
        ClaudeProvider(claude_client(handler)).structured(LLMTask(), "s", "p", TriageBatch)


def sse(text: str, stop_reason: str) -> str:
    events = [
        ("message_start", {"type": "message_start", "message": {**message([], None), "usage": {"input_tokens": 5, "output_tokens": 1}}}),
        ("content_block_start", {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}}),
        ("content_block_delta", {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": text}}),
        ("content_block_stop", {"type": "content_block_stop", "index": 0}),
        ("message_delta", {"type": "message_delta", "delta": {"stop_reason": stop_reason, "stop_sequence": None}, "usage": {"output_tokens": 3}}),
        ("message_stop", {"type": "message_stop"}),
    ]
    return "".join(f"event: {name}\ndata: {json.dumps(data)}\n\n" for name, data in events)


def test_text_resumes_after_pause_turn():
    bodies = []

    def handler(request):
        bodies.append(json.loads(request.content))
        text, stop = ("Part one. ", "pause_turn") if len(bodies) == 1 else ("Part two.", "end_turn")
        return httpx2.Response(200, text=sse(text, stop), headers={"content-type": "text/event-stream"})

    memo = ClaudeProvider(claude_client(handler)).text(LLMTask(effort="high"), "s", "research TSM", search=True)

    assert memo == "Part one. Part two."
    assert [t["type"] for t in bodies[0]["tools"]] == ["web_search_20260209", "web_fetch_20260209"]
    assert bodies[1]["messages"][1]["role"] == "assistant"  # the paused turn is sent back to resume
    assert bodies[1]["messages"][1]["content"][0]["text"] == "Part one. "


class FakeResponse:
    def __init__(self, data):
        self.status_code = 200
        self._data = data
        self.text = json.dumps(data)

    def json(self):
        return self._data


class FakeSession:
    def __init__(self, reply_text):
        self.reply_text = reply_text
        self.calls = []

    def post(self, url, json=None, headers=None, timeout=None):
        self.calls.append({"url": url, "json": json, "headers": headers})
        return FakeResponse({
            "output": [
                {"type": "x_search_call"},
                {"type": "message", "content": [{
                    "type": "output_text", "text": self.reply_text,
                    "annotations": [{"type": "url_citation", "url": "https://x.com/a/status/1"}],
                }]},
            ],
            "citations": ["https://example.com/news"],
        })


def test_grok_search_request_and_parsing():
    session = FakeSession("```json\n" + json.dumps(TRIAGE) + "\n```")
    grok = GrokProvider(api_key="k", x_handles=[f"h{i}" for i in range(12)], session=session)
    result = grok.structured(LLMTask(provider="grok", model="grok-4.7"), "s", "p", TriageBatch,
                             search=True, search_since="2026-09-23T00:00:00+00:00")
    body = session.calls[0]["json"]
    assert session.calls[0]["url"] == "https://api.x.ai/v1/responses"
    assert body["tools"][0] == {"type": "x_search", "allowed_x_handles": [f"h{i}" for i in range(10)],
                                "from_date": "2026-09-23"}
    assert body["tools"][1] == {"type": "web_search"}
    assert result.results[0].item_id == "n1"

    text = grok.text(LLMTask(provider="grok", model="grok-4.7"), "s", "p")
    assert "https://example.com/news" in text and "https://x.com/a/status/1" in text


def test_extract_json_tolerates_prose():
    assert extract_json('Here you go: {"a": 1} thanks') == {"a": 1}
    assert extract_json("[1, 2]") == [1, 2]
