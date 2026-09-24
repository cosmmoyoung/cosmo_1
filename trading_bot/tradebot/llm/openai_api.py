"""OpenAI API provider (GPT-6 family) via the Responses API, billed per token.

Used by default for the always-on stages (news triage, thesis updates, daily
screens) with the cheaper GPT-6 models. Structured stages use strict JSON-schema
outputs, and the reply is validated again locally.
"""

from __future__ import annotations

import os
from typing import Any

import requests
from pydantic import ValidationError

from tradebot.config import LLMTask
from tradebot.llm import LLMError, T, Usage
from tradebot.llm.responses_api import (
    REASONING_EFFORT,
    extract_json,
    parse_output,
    post_responses,
    responses_usage,
    strict_json_schema,
)

OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"


class OpenAIProvider:
    def __init__(self, api_key: str | None = None, session: requests.Session | None = None, timeout: float = 600):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        if not self.api_key:
            raise LLMError("OPENAI_API_KEY is not set (needed for stages that use provider: openai)")
        self.session = session or requests.Session()
        self.timeout = timeout
        self.last_usage: Usage | None = None
        self._no_reasoning: set[str] = set()  # models that rejected the reasoning parameter

    def _body(self, task: LLMTask, system: str, prompt: str, *, search: bool,
              text_format: dict | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": task.model,
            "instructions": system,
            "input": prompt,
            "max_output_tokens": task.max_tokens,
        }
        if task.effort and task.model not in self._no_reasoning:
            body["reasoning"] = {"effort": REASONING_EFFORT[task.effort]}
        if search:
            body["tools"] = [{"type": "web_search"}]
        if text_format:
            body["text"] = {"format": text_format}
        return body

    def _create(self, body: dict[str, Any]) -> dict:
        try:
            data = post_responses(self.session, OPENAI_RESPONSES_URL, self.api_key, body, self.timeout, "OpenAI")
        except LLMError as exc:
            message = str(exc).lower()
            if "reasoning" not in body or "http 400" not in message or "reasoning" not in message:
                raise
            # Some models do not take a reasoning effort: remember that and retry without it.
            self._no_reasoning.add(body["model"])
            data = post_responses(
                self.session, OPENAI_RESPONSES_URL, self.api_key,
                {k: v for k, v in body.items() if k != "reasoning"}, self.timeout, "OpenAI",
            )
        self.last_usage = responses_usage(data)
        if data.get("status") == "incomplete":
            raise LLMError(f"OpenAI reply incomplete ({data.get('incomplete_details')}); raise max_tokens for this stage")
        return data

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        text_format = {"type": "json_schema", "name": schema.__name__, "schema": strict_json_schema(schema), "strict": True}
        reply, _citations = parse_output(self._create(self._body(task, system, prompt, search=search, text_format=text_format)))
        try:
            return schema.model_validate(extract_json(reply))
        except (ValueError, ValidationError) as exc:
            raise LLMError(f"OpenAI did not return a valid {schema.__name__}: {exc}") from exc

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        reply, citations = parse_output(self._create(self._body(task, system, prompt, search=search)))
        if citations:
            reply += "\n\nSources:\n" + "\n".join(f"- {url}" for url in citations)
        return reply
