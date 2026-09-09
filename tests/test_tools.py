from desktop_agent.tools import ToolRegistry, ToolSpec


def test_tools_are_namespaced_and_callable() -> None:
    registry = ToolRegistry()
    registry.register(ToolSpec("math", "add", "add", lambda a: a["a"] + a["b"]))
    registry.register(ToolSpec("other", "add", "other add", lambda a: -1))
    assert registry.call("math__add", {"a": 2, "b": 3}) == 5
    assert {row["function"]["name"] for row in registry.schemas()} == {"math__add", "other__add"}
