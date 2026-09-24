"""Deterministic stand-in provider for tests and `tradebot demo` (no API keys, no cost)."""

from __future__ import annotations

from typing import Callable

from pydantic import BaseModel

from tradebot.config import LLMTask
from tradebot.llm import LLMError, T

StructuredResponder = Callable[[str, str], BaseModel]  # (system, prompt) -> model instance
TextResponder = Callable[[str, str], str]  # (system, prompt) -> memo


class FakeProvider:
    def __init__(self, structured: dict[str, StructuredResponder] | None = None,
                 text: TextResponder | None = None):
        self._structured = structured or {}
        self._text = text
        self.calls: list[str] = []

    def structured(self, task: LLMTask, system: str, prompt: str, schema: type[T], *,
                   search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> T:
        self.calls.append(schema.__name__)
        responder = self._structured.get(schema.__name__)
        if responder is None:
            raise LLMError(f"FakeProvider has no responder for {schema.__name__}")
        return schema.model_validate(responder(system, prompt).model_dump())

    def text(self, task: LLMTask, system: str, prompt: str, *,
             search: bool = False, search_since: str | None = None, max_search_uses: int = 12) -> str:
        self.calls.append("text")
        if self._text is None:
            return "(fake memo)\n\nVERDICT: PASS"
        return self._text(system, prompt)
