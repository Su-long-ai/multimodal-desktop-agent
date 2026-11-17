# Multimodal Desktop Agent

**Agent engineering portfolio project:** a testable orchestration core for a Windows desktop AI agent with pluggable LLM providers, long-term memory, MCP-style tools, and optional voice/avatar adapters.

**Recruiter quick scan**
- **Agent runtime:** provider abstraction + bounded tool-execution loop
- **Tooling:** collision-safe MCP-style namespaces and adapter boundaries
- **Memory:** pluggable long-term backend with deterministic in-memory fallback
- **Multimodal integration:** STT/TTS/avatar interfaces kept outside the core
- **Engineering:** dependency injection, offline tests, privacy-conscious public/private boundary

## Why this repository exists

A desktop agent quickly becomes more than a chat window.  GUI event loops, streaming model calls, tool servers, memory services, microphone/audio pipelines and avatar state all have different failure modes.  This extraction makes the boundaries explicit and unit-testable.

## Architecture

```text
user text / optional STT
          |
          v
   AgentOrchestrator <---- recalled memory
          |
          +----> LLMProvider (Ollama / OpenAI-compatible / test double)
          |               |
          |               +---- tool calls ----> ToolRegistry ----> MCP-style adapters
          |                                      |
          |                                      +---- namespaced tools
          |
          +----> MemoryBackend (long-term adapter or InMemory fallback)
          +----> AvatarAdapter (optional desktop/avatar implementation)
          +----> TTS/STT interfaces (optional voice implementation)
```

The public package imports **no microphone, GUI, GPU, Live2D or network library at module import time**.  Those capabilities belong in optional adapters so the core stays testable offline.

## Included

- validated, non-secret runtime configuration and a small migration path from an older Ollama layout;
- dependency-injected LLM interface plus an OpenAI-compatible request parser/builder;
- memory abstraction with deterministic in-memory fallback;
- collision-safe tool namespacing for multiple MCP-like servers;
- bounded tool-execution loop;
- STT/TTS and avatar interfaces without private assets;
- offline console demo and unit tests.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"
pytest
python examples/console_agent.py
```

No API key or network access is required for the tests or console demo.

## Security and privacy

The core config stores only the **name of the environment variable** holding an API key.  Real applications should additionally encrypt or OS-protect local settings, redact secrets from logs, obtain explicit consent before screen/microphone capture, and minimize retention of voiceprints or personal memories.  See [docs/SECURITY_PRIVACY.md](docs/SECURITY_PRIVACY.md).

## Public/private boundary

No avatar model, personal voice sample, speaker reference, local STT model, chat history, API credential, screenshot, machine path or generated log is part of this repository.  See [docs/PRIVATE_TO_PUBLIC_BOUNDARY.md](docs/PRIVATE_TO_PUBLIC_BOUNDARY.md).

## Limitations

This public repo is the testable orchestration layer, not the full desktop GUI.  Optional PySide/Live2D, Hindsight, SenseVoice/VAD and production MCP transports remain adapter work.  The repository demonstrates engineering boundaries; it does not claim benchmark performance for speech, memory or model quality.

## License

MIT for code in this repository.  External models, avatar assets and services retain their own licenses and are not redistributed here.
