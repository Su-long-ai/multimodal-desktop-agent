from __future__ import annotations

from dataclasses import dataclass
import json
import os
from typing import Callable, Mapping, Protocol, Sequence, Any

from .config import AgentConfig
from .models import ChatMessage, LLMResponse, ToolCall


class LLMProvider(Protocol):
    def complete(self, messages: Sequence[ChatMessage], tools: Sequence[Mapping[str, Any]]) -> LLMResponse: ...


class EchoProvider:
    """Offline provider used by tests and the console demo."""

    def complete(self, messages: Sequence[ChatMessage], tools: Sequence[Mapping[str, Any]]) -> LLMResponse:
        last = next((message.content for message in reversed(messages) if message.role == "user"), "")
        return LLMResponse(content=f"echo: {last}")


@dataclass(slots=True)
class OpenAICompatibleProvider:
    """OpenAI-compatible request builder with an injectable transport.

    ``transport`` receives URL, headers, JSON payload and timeout.  Keeping it
    injectable makes unit tests offline and lets a desktop app choose requests,
    httpx or another networking layer without coupling the orchestration core.
    """

    config: AgentConfig
    transport: Callable[[str, Mapping[str, str], Mapping[str, Any], float], Mapping[str, Any]]

    def complete(self, messages: Sequence[ChatMessage], tools: Sequence[Mapping[str, Any]]) -> LLMResponse:
        key = os.environ.get(self.config.api_key_env, "").strip()
        headers = {"Content-Type": "application/json"}
        if key:
            headers["Authorization"] = f"Bearer {key}"
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": [
                {k: v for k, v in {"role": m.role, "content": m.content, "name": m.name}.items() if v is not None}
                for m in messages
            ],
        }
        if tools:
            payload["tools"] = list(tools)
        raw = self.transport(
            self.config.api_base + "/chat/completions",
            headers,
            payload,
            self.config.request_timeout_seconds,
        )
        return parse_openai_compatible_response(raw)


def parse_openai_compatible_response(raw: Mapping[str, Any]) -> LLMResponse:
    try:
        message = raw["choices"][0]["message"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ValueError("invalid OpenAI-compatible response") from exc
    calls: list[ToolCall] = []
    for item in message.get("tool_calls") or []:
        function = item.get("function") or {}
        arguments = function.get("arguments") or "{}"
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError as exc:
                raise ValueError("tool-call arguments are not valid JSON") from exc
        if not isinstance(arguments, Mapping):
            raise ValueError("tool-call arguments must decode to an object")
        calls.append(ToolCall(str(function.get("name") or ""), dict(arguments), item.get("id")))
    return LLMResponse(content=str(message.get("content") or ""), tool_calls=tuple(calls))
