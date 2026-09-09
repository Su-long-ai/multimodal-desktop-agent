from desktop_agent.config import AgentConfig
from desktop_agent.llm import EchoProvider
from desktop_agent.memory import InMemoryMemory
from desktop_agent.orchestrator import AgentOrchestrator
from desktop_agent.tools import ToolRegistry, ToolSpec


def main() -> None:
    tools = ToolRegistry()
    tools.register(ToolSpec("local", "add", "Add two numbers", lambda a: {"sum": a.get("a", 0) + a.get("b", 0)}))
    agent = AgentOrchestrator(
        config=AgentConfig(provider="mock", api_base="http://localhost", model="echo"),
        llm=EchoProvider(),
        memory=InMemoryMemory(),
        tools=tools,
    )
    print(agent.respond("hello from the offline console demo"))


if __name__ == "__main__":
    main()
