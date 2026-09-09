from desktop_agent.config import AgentConfig
from desktop_agent.memory import InMemoryMemory
from desktop_agent.models import LLMResponse, ToolCall
from desktop_agent.orchestrator import AgentOrchestrator
from desktop_agent.tools import ToolRegistry, ToolSpec


class ScriptedLLM:
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, messages, tools):
        self.calls += 1
        if self.calls == 1:
            return LLMResponse(tool_calls=(ToolCall("math__add", {"a": 2, "b": 5}),))
        assert any(message.role == "tool" and message.content == "7" for message in messages)
        return LLMResponse(content="the result is 7")


def test_orchestrator_executes_bounded_tool_loop_and_retains_memory() -> None:
    registry = ToolRegistry()
    registry.register(ToolSpec("math", "add", "add", lambda a: a["a"] + a["b"]))
    memory = InMemoryMemory()
    agent = AgentOrchestrator(
        config=AgentConfig(provider="mock", api_base="http://localhost", model="scripted"),
        llm=ScriptedLLM(),
        memory=memory,
        tools=registry,
    )
    assert agent.respond("add two and five") == "the result is 7"
    assert memory.recall("result 7")
