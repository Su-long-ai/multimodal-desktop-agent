from __future__ import annotations

import json
from typing import Sequence

from .avatar import AvatarAdapter, NullAvatar
from .config import AgentConfig
from .llm import LLMProvider
from .memory import MemoryBackend
from .models import ChatMessage
from .tools import ToolRegistry


class AgentOrchestrator:
    """Small dependency-injected agent loop with bounded tool rounds."""

    def __init__(
        self,
        *,
        config: AgentConfig,
        llm: LLMProvider,
        memory: MemoryBackend,
        tools: ToolRegistry | None = None,
        avatar: AvatarAdapter | None = None,
    ) -> None:
        self.config = config
        self.llm = llm
        self.memory = memory
        self.tools = tools or ToolRegistry()
        self.avatar = avatar or NullAvatar()
        self.history: list[ChatMessage] = []

    def _context_messages(self, user_text: str) -> list[ChatMessage]:
        messages = list(self.history)
        if self.config.memory_enabled:
            recalled = self.memory.recall(user_text, limit=5)
            if recalled:
                context = "\n".join(f"- {item.text}" for item in recalled)
                messages.append(ChatMessage("system", "Relevant remembered context:\n" + context))
        messages.append(ChatMessage("user", user_text))
        return messages

    def respond(self, user_text: str) -> str:
        user_text = user_text.strip()
        if not user_text:
            raise ValueError("user_text must not be empty")
        messages = self._context_messages(user_text)
        response = self.llm.complete(messages, self.tools.schemas())

        for _ in range(self.config.max_tool_rounds):
            if not response.tool_calls:
                break
            messages.append(ChatMessage("assistant", response.content))
            for call in response.tool_calls:
                result = self.tools.call(call.name, call.arguments)
                messages.append(
                    ChatMessage(
                        "tool",
                        json.dumps(result, ensure_ascii=False, default=str),
                        name=call.name,
                    )
                )
            response = self.llm.complete(messages, self.tools.schemas())
        else:
            if response.tool_calls:
                raise RuntimeError("tool round limit exceeded")

        text = response.content.strip()
        self.history.extend([ChatMessage("user", user_text), ChatMessage("assistant", text)])
        if self.config.memory_enabled:
            self.memory.retain(f"User: {user_text}\nAssistant: {text}", importance=0.4)
        return text
