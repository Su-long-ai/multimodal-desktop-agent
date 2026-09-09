from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class MemoryItem:
    text: str
    importance: float = 0.5


class MemoryBackend(Protocol):
    def recall(self, query: str, *, limit: int = 5) -> list[MemoryItem]: ...
    def retain(self, text: str, *, importance: float = 0.5) -> None: ...
    def clear(self) -> None: ...


class InMemoryMemory:
    """Simple deterministic fallback when a long-term memory service is unavailable."""

    def __init__(self) -> None:
        self._items: list[MemoryItem] = []

    def recall(self, query: str, *, limit: int = 5) -> list[MemoryItem]:
        tokens = {token.lower() for token in query.split() if token.strip()}
        if not tokens:
            return list(reversed(self._items[-limit:]))
        scored: list[tuple[int, int, MemoryItem]] = []
        for index, item in enumerate(self._items):
            text_tokens = {token.lower() for token in item.text.split()}
            scored.append((len(tokens & text_tokens), index, item))
        scored.sort(key=lambda row: (row[0], row[1]), reverse=True)
        return [item for overlap, _, item in scored if overlap > 0][:limit]

    def retain(self, text: str, *, importance: float = 0.5) -> None:
        text = text.strip()
        if not text:
            return
        self._items.append(MemoryItem(text=text, importance=max(0.0, min(float(importance), 1.0))))

    def clear(self) -> None:
        self._items.clear()
