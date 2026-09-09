from desktop_agent.config import AgentConfig


def test_old_ollama_fields_migrate_without_secrets() -> None:
    config = AgentConfig.from_mapping({
        "ollama_url": "http://127.0.0.1:11434/api/chat",
        "ollama_model": "demo-model",
        "api_key": "must-be-ignored",
    })
    assert config.api_base == "http://127.0.0.1:11434/v1"
    assert config.model == "demo-model"
    assert not hasattr(config, "api_key")


def test_invalid_scheme_is_rejected() -> None:
    try:
        AgentConfig(api_base="file:///tmp/model")
    except ValueError:
        return
    raise AssertionError("invalid URL scheme was accepted")
