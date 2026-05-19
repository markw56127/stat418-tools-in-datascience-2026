from agent import ReActAgent


def test_agent_weather_task() -> None:
    agent = ReActAgent()
    result = agent.run("What's the weather in San Francisco?")
    assert "San Francisco" in result.final_answer
    assert "chance of rain" in result.final_answer
    assert len(result.steps) == 1
    assert result.steps[0].action == "get_weather"


def test_agent_database_search() -> None:
    agent = ReActAgent()
    result = agent.run("Search the database for laptop options")
    assert "Laptop" in result.final_answer or "Notebook" in result.final_answer
    assert result.steps[0].action == "search_database"


def test_agent_fallback_response() -> None:
    agent = ReActAgent()
    result = agent.run("Write me a poem")
    assert "weather questions" in result.final_answer
    assert result.steps[0].action is None

# Made with Bob
