"""Shared helpers for OpenAI-style Responses APIs (OpenAI and xAI) and for JSON replies."""

from __future__ import annotations

import copy
import json
import re
from typing import Any

import requests
from pydantic import BaseModel

from tradebot.llm import LLMError, LLMQuotaExceeded, LLMRefusal, Usage

# Our effort names -> the reasoning-effort names OpenAI-style APIs and Codex accept.
REASONING_EFFORT = {"low": "low", "medium": "medium", "high": "high", "xhigh": "xhigh", "max": "xhigh"}


def post_responses(session: requests.Session, url: str, api_key: str, body: dict, timeout: float,
                   vendor: str) -> dict:
    resp = session.post(url, json=body, timeout=timeout, headers={"Authorization": f"Bearer {api_key}"})
    if resp.status_code == 429:
        raise LLMQuotaExceeded(f"{vendor} HTTP 429 (rate limit or quota): {resp.text[:300]}")
    if resp.status_code != 200:
        raise LLMError(f"{vendor} HTTP {resp.status_code}: {resp.text[:300]}")
    return resp.json()


def parse_output(data: dict) -> tuple[str, list[str]]:
    """(reply text, cited URLs) from a Responses API payload."""
    texts: list[str] = []
    urls: list[str] = []
    for cite in data.get("citations") or []:
        url = cite.get("url") if isinstance(cite, dict) else cite
        if isinstance(url, str):
            urls.append(url)
    for item in data.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "refusal":
                raise LLMRefusal(f"model declined: {part.get('refusal', '')[:200]}")
            if part.get("type") == "output_text":
                texts.append(part.get("text", ""))
                urls.extend(a["url"] for a in part.get("annotations", []) if a.get("url"))
    return "\n".join(texts).strip(), list(dict.fromkeys(urls))


def responses_usage(data: dict) -> Usage:
    usage = data.get("usage") or {}
    cached = (usage.get("input_tokens_details") or {}).get("cached_tokens", 0)
    return Usage(
        input_tokens=usage.get("input_tokens", 0),
        cached_input_tokens=cached or 0,
        output_tokens=usage.get("output_tokens", 0),
    )


def extract_json(text: str) -> Any:
    """Parse the first JSON object or array in a model reply (tolerates code fences and prose)."""
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    starts = [i for i in (cleaned.find("{"), cleaned.find("[")) if i != -1]
    if not starts:
        raise ValueError("no JSON found in reply")
    start = min(starts)
    end = cleaned.rfind("}" if cleaned[start] == "{" else "]")
    return json.loads(cleaned[start:end + 1])


def strict_json_schema(model: type[BaseModel]) -> dict:
    """Pydantic schema -> the strict form OpenAI structured outputs (and Codex) require:
    every object closed (additionalProperties false) and every property listed as required."""
    schema = copy.deepcopy(model.model_json_schema())

    def fix(node: Any) -> None:
        if isinstance(node, dict):
            node.pop("default", None)
            if "$ref" in node:  # a $ref must stand alone
                for key in [k for k in node if k != "$ref"]:
                    node.pop(key)
            if node.get("type") == "object" and "properties" in node:
                node["additionalProperties"] = False
                node["required"] = list(node["properties"])
            for value in node.values():
                fix(value)
        elif isinstance(node, list):
            for value in node:
                fix(value)

    fix(schema)
    return schema
