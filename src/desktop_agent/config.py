from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Mapping
from urllib.parse import urlparse


@dataclass(frozen=True, slots=True)
class AgentConfig:
    """Validated non-secret runtime configuration.

    Secrets are referenced by environment-variable name instead of being stored
    in this object.  The private application can layer a GUI/config file on top.
    """

    provider: str = "ollama"
    api_base: str = "http://127.0.0.1:11434/v1"
    model: str = "local-model"
    api_key_env: str = "DESKTOP_AGENT_API_KEY"
    memory_enabled: bool = True
    max_tool_rounds: int = 2
    request_timeout_seconds: float = 45.0

    def __post_init__(self) -> None:
        provider = self.provider.strip().lower()
        if provider not in {"ollama", "openai-compatible", "mock"}:
            raise ValueError(f"unsupported provider: {self.provider}")
        parsed = urlparse(self.api_base)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("api_base must be an http(s) URL")
        if not self.model.strip():
            raise ValueError("model must not be empty")
        if not self.api_key_env.strip():
            raise ValueError("api_key_env must not be empty")
        if not 0 <= self.max_tool_rounds <= 8:
            raise ValueError("max_tool_rounds must be between 0 and 8")
        if not 1 <= self.request_timeout_seconds <= 300:
            raise ValueError("request_timeout_seconds must be between 1 and 300")
        object.__setattr__(self, "provider", provider)
        object.__setattr__(self, "api_base", self.api_base.rstrip("/"))

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "AgentConfig":
        """Load known fields only, with a tiny migration for older names."""

        data = dict(raw)
        if "ollama_url" in data and "api_base" not in data:
            url = str(data.pop("ollama_url"))
            if url.endswith("/api/chat"):
                url = url[: -len("/api/chat")] + "/v1"
            data["api_base"] = url
            data.setdefault("provider", "ollama")
        if "ollama_model" in data and "model" not in data:
            data["model"] = data.pop("ollama_model")
        allowed = {field.name for field in fields(cls)}
        return cls(**{key: value for key, value in data.items() if key in allowed})
