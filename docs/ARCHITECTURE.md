# Architecture

## Core principle: dependency inversion

The orchestrator knows about protocols, not concrete GUI/audio/network libraries.  This avoids a single monolithic file owning every subsystem and makes failure paths testable.

### `config.py`
Validates non-secret runtime options.  Credentials are referenced by environment-variable name.  Migrations are narrow and explicit.

### `llm.py`
`LLMProvider` is the completion boundary. `OpenAICompatibleProvider` receives an injected transport, so request construction/parsing can be tested without the network.

### `tools.py`
Each tool is qualified as `server__tool`.  This prevents collisions when multiple MCP-like servers export common names such as `search` or `read`.

### `memory.py`
`MemoryBackend` hides the long-term memory implementation. `InMemoryMemory` is an immediate fallback for offline or failed-service operation.

### `orchestrator.py`
Owns bounded tool rounds, message history and memory recall/retention.  The loop is deliberately capped to avoid runaway tool recursion.

### Optional adapters
GUI, avatar rendering, STT, TTS, VAD, speaker verification, screen capture and real MCP transports should live outside the core package and be loaded only when configured.

## Failure isolation

A production desktop app should put GUI, model I/O, memory I/O, audio and external tools on separate concurrency boundaries with cancellation and timeouts.  The public core models those boundaries without taking a dependency on a particular event loop.
