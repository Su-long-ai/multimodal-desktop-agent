from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping


@dataclass(frozen=True, slots=True)
class ToolSpec:
    server: str
    name: str
    description: str
    handler: Callable[[Mapping[str, Any]], Any]

    @property
    def qualified_name(self) -> str:
        return f"{self.server}__{self.name}"


class ToolRegistry:
    """Collision-safe registry for tools coming from multiple MCP-like servers."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        name = spec.qualified_name
        if name in self._tools:
            raise ValueError(f"duplicate tool: {name}")
        if not spec.server or not spec.name:
            raise ValueError("server and name must be non-empty")
        self._tools[name] = spec

    def schemas(self) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": spec.description,
                    "parameters": {"type": "object", "additionalProperties": True},
                },
            }
            for name, spec in sorted(self._tools.items())
        ]

    def call(self, qualified_name: str, arguments: Mapping[str, Any]) -> Any:
        try:
            tool = self._tools[qualified_name]
        except KeyError as exc:
            raise KeyError(f"unknown tool: {qualified_name}") from exc
        return tool.handler(dict(arguments))
