"""Claude provider (Anthropic Python SDK).

- Structured stages use `client.beta.messages.parse(output_format=Model)`, so the
  reply is validated against the pydantic model before the pipeline sees it.
- Research memos stream (they can be long) and may use the server-side
  web_search / web_fetch tools; `pause_turn` is resumed automatically.
- Opus 5 / Fable 5.1 requests opt into server-side refusal fallbacks
  (`fallbacks="default"`), so a false-positive safety decline is retried on the
  model Anthropic recommends instead of failing the whole pipeline step.
"""

from __future__ import annotations

from typing import Any

import anthropic

from tradebot.config import LLMTask
from tradebot.llm import LLMError, LLMRefusal, T

FALLBACK_BETA = "server-side-fallback-2026-07-01"
FALLBACK_MODELS = {"claude-opus-5", "claude-opus-5-5", "claude-fable-5-1"}
WEB_TOOLS = (
    {"type": "web_search_20260209", "name": "web_search"},
    {"type": "web_fetch_20260209", "name": "web_fetch"},
)
MAX_CONTINUATIONS = 8


def _raise_for_stop(response: Any) -> None:
    reason = response.stop_reason
    if reason == "refusal":
        details = getattr(response, "stop_details", None)
        category = getattr(details, "category", None) if details else None
        raise LLMRefusal(f"{response.model} declined the request (category={category})")
    if reason in ("max_tokens", "model_context_window_exceeded"):
        raise LLMError(f"{response.model} stopped with {reason}; raise max_tokens for this stage in config.yaml")


class ClaudeProvider:
    def __init__(self, client: anthropic.Anthropic | None = None):
        # Credentials resolve from ANTHROPIC_API_KEY or an `ant auth login` profile.
        self.client = client or anthropic.Anthropic(max_retries=4)

    def _request(self, task: LLMTask, system: str) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": task.model,
            "max_tokens": task.max_tokens,
            # Stable system prompts first so repeated calls hit the prompt cache.
            "system": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        }
        if not task.model.startswith("claude-haiku"):
            request["thinking"] = {"type": "adaptive"}
            if task.effort:
                request["output_config"] = {"effort": task.effort}
        if task.model in FALLBACK_MODELS:
            request["fallbacks"] = "default"
            request["betas"] = [FALLBACK_BETA]
        return request

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        if search:
            # Gather evidence with the web tools first, then convert it into the schema
            # in a separate tool-free call.
            notes = self.text(task, system, prompt, search=True, max_search_uses=max_search_uses)
            prompt = f"{prompt}\n\n<research_notes>\n{notes}\n</research_notes>\n\nUse the research notes above to produce the answer."
        response = self.client.beta.messages.parse(
            messages=[{"role": "user", "content": prompt}],
            output_format=schema,
            **self._request(task, system),
        )
        _raise_for_stop(response)
        if response.parsed_output is None:
            raise LLMError(f"{task.model} returned no parseable {schema.__name__}")
        return response.parsed_output

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        request = self._request(task, system)
        if search:
            request["tools"] = [{**tool, "max_uses": max_search_uses} for tool in WEB_TOOLS]
        user = {"role": "user", "content": prompt}
        assistant_blocks: list[Any] = []
        texts: list[str] = []
        for _ in range(MAX_CONTINUATIONS):
            messages = [user]
            if assistant_blocks:
                messages.append({"role": "assistant", "content": assistant_blocks})
            with self.client.beta.messages.stream(messages=messages, **request) as stream:
                response = stream.get_final_message()
            _raise_for_stop(response)
            texts.extend(block.text for block in response.content if block.type == "text")
            if response.stop_reason != "pause_turn":
                return "".join(texts).strip()
            # The server-side tool loop paused; send the turn back so it resumes where it stopped.
            assistant_blocks = assistant_blocks + list(response.content)
        raise LLMError(f"{task.model}: web research did not finish after {MAX_CONTINUATIONS} continuations")
