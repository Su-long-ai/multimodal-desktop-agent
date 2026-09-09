# Private-to-Public Boundary

The working private desktop application includes integrations and local assets that should not be copied into a portfolio repository.

## Excluded

- Live2D/avatar model files and textures;
- personal voice references or voiceprints;
- local STT/model directories and checkpoints;
- API keys, provider settings and private MCP headers/environment variables;
- screenshots, chat histories, remembered personal facts and debug audio;
- generated logs, caches and machine-specific absolute paths;
- provider-specific private configuration.

## Published here

Only original orchestration code, generic interfaces, synthetic/offline test doubles and documentation.

A future GUI adapter can be open-sourced separately if its model/assets are independently licensed for redistribution.
