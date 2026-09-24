"""Grok provider (xAI Responses API, raw HTTP).

Grok's edge for this bot is real-time X (Twitter) coverage, so it is used as the
news scout: `search=True` turns on xAI's server-side `x_search` and `web_search`
tools. Structured replies are requested in the prompt and validated locally.
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests
from pydantic import ValidationError

from tradebot.config import LLMTask
from tradebot.llm import LLMError, T, Usage
from tradebot.llm.responses_api import extract_json, parse_output, post_responses, responses_usage

__all__ = ["GrokProvider", "extract_json"]

XAI_RESPONSES_URL = "https://api.x.ai/v1/responses"
MAX_X_HANDLES = 10


class GrokProvider:
    def __init__(self, api_key: str | None = None, x_handles: list[str] | None = None,
                 session: requests.Session | None = None, timeout: float = 300):
        self.api_key = api_key or os.environ.get("XAI_API_KEY", "")
        if not self.api_key:
            raise LLMError("XAI_API_KEY is not set (needed for the Grok scout)")
        self.x_handles = list(x_handles or [])[:MAX_X_HANDLES]
        self.session = session or requests.Session()
        self.timeout = timeout
        self.last_usage: Usage | None = None

    def ask(self, model: str, system: str, prompt: str, *, search: bool = False,
            search_since: str | None = None) -> tuple[str, list[str]]:
        body: dict[str, Any] = {
            "model": model,
            "input": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        }
        if search:
            x_search: dict[str, Any] = {"type": "x_search"}
            if self.x_handles:
                x_search["allowed_x_handles"] = self.x_handles
            if search_since:
                x_search["from_date"] = search_since[:10]
            body["tools"] = [x_search, {"type": "web_search"}]
        data = post_responses(self.session, XAI_RESPONSES_URL, self.api_key, body, self.timeout, "xAI")
        usage = responses_usage(data)
        self.last_usage = usage if self.last_usage is None else self.last_usage + usage
        return parse_output(data)

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        schema_json = json.dumps(schema.model_json_schema(), ensure_ascii=False)
        request = (
            f"{prompt}\n\nReply with a single JSON object (no prose, no code fences) that "
            f"validates against this JSON Schema:\n{schema_json}"
        )
        error: Exception | None = None
        for _ in range(2):
            reply, _citations = self.ask(task.model, system, request, search=search, search_since=search_since)
            try:
                return schema.model_validate(extract_json(reply))
            except (ValueError, ValidationError) as exc:
                error = exc
                request += "\n\nYour previous reply did not match the schema. Reply again with only the JSON object."
        raise LLMError(f"Grok did not return a valid {schema.__name__}: {error}")

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        reply, citations = self.ask(task.model, system, prompt, search=search, search_since=search_since)
        if citations:
            reply += "\n\nSources:\n" + "\n".join(f"- {url}" for url in citations)
        return reply
