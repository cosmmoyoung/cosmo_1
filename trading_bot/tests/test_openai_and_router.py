"""OpenAI API provider, strict schemas, and the router's usage log and quota fallback."""

import json

import pytest

from tradebot.config import LLMConfig, LLMTask
from tradebot.llm import LLMQuotaExceeded, LLMRefusal, LLMRouter, Usage
from tradebot.llm.fake import FakeProvider
from tradebot.llm.openai_api import OpenAIProvider
from tradebot.llm.responses_api import strict_json_schema
from tradebot.models import ThesisDraft, TriageBatch, TriageResult

TRIAGE = {"results": [{
    "item_id": "n1", "materiality": 3, "tickers": [], "industries": [],
    "event_type": "other", "summary": "noise", "route": "ignore",
}]}


class Resp:
    def __init__(self, status, data):
        self.status_code = status
        self._data = data
        self.text = json.dumps(data)

    def json(self):
        return self._data


class Session:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.bodies = []

    def post(self, url, json=None, headers=None, timeout=None):
        self.bodies.append(json)
        return self.responses.pop(0)


def ok(text, usage=None):
    return Resp(200, {
        "status": "completed",
        "output": [{"type": "reasoning"}, {"type": "message", "content": [{"type": "output_text", "text": text}]}],
        "usage": usage or {"input_tokens": 1000, "input_tokens_details": {"cached_tokens": 200}, "output_tokens": 300},
    })


def test_openai_structured_request():
    session = Session(ok(json.dumps(TRIAGE)))
    provider = OpenAIProvider(api_key="k", session=session)
    result = provider.structured(LLMTask(provider="openai", model="gpt-6-luna", effort="low"), "SYS", "PROMPT", TriageBatch)
    body = session.bodies[0]
    assert result.results[0].route == "ignore"
    assert body["model"] == "gpt-6-luna" and body["instructions"] == "SYS" and body["input"] == "PROMPT"
    assert body["reasoning"] == {"effort": "low"}
    fmt = body["text"]["format"]
    assert fmt["type"] == "json_schema" and fmt["strict"] is True and fmt["name"] == "TriageBatch"
    assert fmt["schema"]["additionalProperties"] is False
    assert (provider.last_usage.input_tokens, provider.last_usage.cached_input_tokens, provider.last_usage.output_tokens) == (1000, 200, 300)


def test_openai_retries_without_reasoning_when_model_rejects_it():
    session = Session(Resp(400, {"error": {"message": "Unsupported parameter: 'reasoning.effort'"}}), ok("hello"))
    provider = OpenAIProvider(api_key="k", session=session)
    assert provider.text(LLMTask(provider="openai", model="gpt-6-luna", effort="low"), "S", "P") == "hello"
    assert "reasoning" not in session.bodies[1]
    assert "gpt-6-luna" in provider._no_reasoning


def test_openai_quota_and_refusal():
    with pytest.raises(LLMQuotaExceeded):
        OpenAIProvider(api_key="k", session=Session(Resp(429, {"error": {"code": "insufficient_quota"}}))).text(
            LLMTask(provider="openai", model="gpt-6-sol"), "S", "P")
    refusal = Resp(200, {"status": "completed", "output": [{"type": "message", "content": [{"type": "refusal", "refusal": "no"}]}]})
    with pytest.raises(LLMRefusal):
        OpenAIProvider(api_key="k", session=Session(refusal)).text(LLMTask(provider="openai", model="gpt-6-sol"), "S", "P")


def test_strict_schema_closes_nested_objects_and_keeps_nullables():
    schema = strict_json_schema(ThesisDraft)
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == set(schema["properties"])
    pillar = schema["$defs"]["Pillar"]
    assert pillar["additionalProperties"] is False and set(pillar["required"]) == {"claim", "evidence", "status"}
    assert {"type": "null"} in schema["properties"]["fair_value"]["anyOf"]


def triage_reply(system, prompt):
    return TriageBatch(results=[TriageResult(**TRIAGE["results"][0])])


class QuotaProvider(FakeProvider):
    def structured(self, *args, **kwargs):
        self.calls.append("quota")
        raise LLMQuotaExceeded("window used up")


def test_router_falls_back_on_quota_and_logs_usage():
    backup = FakeProvider({"TriageBatch": triage_reply}, usage=Usage(1_000_000, 0, 100_000))
    cfg = LLMConfig(triage=LLMTask(provider="codex_cli", model="gpt-6-astra",
                                   fallback=LLMTask(provider="openai", model="gpt-6-sol")))
    records = []
    router = LLMRouter(cfg, {"codex_cli": QuotaProvider(), "openai": backup},
                       usage_sink=lambda stage, task, usage, cost: records.append((stage, task.provider, cost)))
    assert router.structured("triage", "S", "P", TriageBatch).results[0].item_id == "n1"
    assert records == [("triage", "openai", pytest.approx(3.0))]  # 1mn input x $2 + 0.1mn output x $10


def test_quota_without_fallback_raises():
    cfg = LLMConfig(triage=LLMTask(provider="codex_cli", model="gpt-6-astra"))
    with pytest.raises(LLMQuotaExceeded):
        LLMRouter(cfg, {"codex_cli": QuotaProvider()}).structured("triage", "S", "P", TriageBatch)


def test_reported_cost_wins_and_cached_input_is_discounted():
    router = LLMRouter(LLMConfig())
    assert router.api_cost("opus", Usage(10, 0, 10, cost_usd=1.23)) == 1.23
    # 1mn tokens, 800k of them cached: 200k x $5 + 800k x $0.5 = $1.40
    assert router.api_cost("claude-opus-5", Usage(1_000_000, 800_000, 0)) == pytest.approx(1.4)
    assert router.api_cost("unknown-model", Usage(1_000_000, 0, 0)) == 0.0


def test_factory_creates_each_provider_once():
    made = []

    def factory(name):
        made.append(name)
        return FakeProvider({"TriageBatch": triage_reply})

    cfg = LLMConfig(triage=LLMTask(provider="openai", model="gpt-6-luna"))
    router = LLMRouter(cfg, factory=factory)
    router.structured("triage", "S", "P", TriageBatch)
    router.with_stages(triage=LLMTask(provider="openai", model="gpt-6-sol")).structured("triage", "S", "P", TriageBatch)
    assert made == ["openai"]
