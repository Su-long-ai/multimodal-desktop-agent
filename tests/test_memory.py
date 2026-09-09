from desktop_agent.memory import InMemoryMemory


def test_memory_recall_and_clear() -> None:
    memory = InMemoryMemory()
    memory.retain("likes local models")
    memory.retain("uses semantic retrieval")
    assert memory.recall("local models")[0].text == "likes local models"
    memory.clear()
    assert memory.recall("local") == []
