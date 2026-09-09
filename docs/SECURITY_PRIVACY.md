# Security and Privacy

Desktop agents can touch sensitive local context.  Treat that authority as a product feature that needs explicit boundaries.

- Keep API credentials in environment variables or OS-backed secret storage; never commit them.
- Redact authorization headers, prompts with secrets and personal file paths from logs.
- Require explicit opt-in for microphone, screen capture, speaker verification and long-term memory.
- Do not upload screenshots, voiceprints or personal memory to an external provider unless the user has configured that provider for the feature.
- Bound tool rounds and tool timeouts.  Surface tool failures rather than silently retrying forever.
- Namespace tool names and validate imported tool configuration.
- Treat model-generated tool arguments as untrusted input; concrete adapters must validate schemas and enforce local authorization.
- Provide a session-only memory fallback when the long-term memory service is unavailable.

This public repository contains no real credentials, personal media, chat logs or biometric reference data.
