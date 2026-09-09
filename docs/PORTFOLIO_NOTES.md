# Portfolio Notes

Evidence-grounded resume bullets for the larger private desktop-agent project:

- Built a Windows desktop AI agent integrating local/OpenAI-compatible LLM chat, long-term memory with session fallback, MCP-style tools, voice input/output and animated-avatar interaction.
- Engineered graceful degradation around optional services: local model endpoints, memory daemon, STT/TTS and tool servers can fail independently without requiring the entire desktop application to stop.
- Integrated multi-provider model requests, streaming/tool-call handling, MCP server configuration, speech activity/recognition pipelines and Windows/PySide desktop interactions in one working application, then extracted the reusable orchestration layer into this modular public codebase.
- Refactored the portfolio-facing architecture around dependency injection, namespaced tools, bounded tool rounds, non-secret configuration, offline tests and explicit privacy boundaries for voice, screen and memory features.

When interviewing, describe the full private app as a working integration project, while using this public repository to demonstrate code organization and engineering judgment.
