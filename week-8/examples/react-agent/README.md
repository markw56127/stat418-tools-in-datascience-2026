# Simple ReAct Agent

A runnable implementation of the ReAct (Reasoning + Acting) agent architecture using local Python tools.

## Overview

This example demonstrates:
- a basic ReAct loop implementation
- local tool calling with simple schemas
- reasoning, action, and observation steps
- fallback behavior when no tool applies
- automated tests for the agent

## Files

- `agent.py` - main ReAct agent implementation
- `tools.py` - tool definitions and implementations
- `test_agent.py` - unit tests for the agent
- `requirements.txt` - Python dependencies

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

This example is intentionally local and deterministic so it can be run during class without API keys.

## Usage

```bash
# Run the agent demo
python agent.py

# Run tests
pytest test_agent.py
```

## Example Interaction

```text
User: What's the weather in San Francisco and should I bring an umbrella?

Thought: I need to get the weather for San Francisco.
Action: get_weather({"location": "San Francisco"})
Observation: {"location": "San Francisco", "temp_f": 65, "conditions": "partly cloudy", "precipitation_chance": 20}

Final Answer: The weather in San Francisco is 65°F and partly cloudy with a 20% chance of rain. You probably do not need an umbrella.
```

## Supported Tools

### `get_weather`
Returns mock weather data for supported cities:
- San Francisco
- Los Angeles
- New York

### `search_database`
Searches a tiny in-memory product catalog for:
- laptops
- audio products
- accessories

## Key Concepts

### ReAct Loop

The agent follows this pattern:
1. **Thought**: reason about what to do next
2. **Action**: call a tool
3. **Observation**: inspect the result
4. **Repeat** until ready to answer
5. **Final Answer**: produce the response

### Tool Definitions

Tools are represented in `tools.py` with both:
- Python functions
- simple JSON-style schemas

This lets students see both the implementation side and the agent-facing description side.

## Extending the Agent

Add new tools by:
1. creating a new function in `tools.py`
2. adding a schema to `TOOL_SCHEMAS`
3. registering it in `TOOLS`
4. updating the routing logic in `agent.py`

## Testing

The test file covers:
- weather requests
- product database search
- unsupported task fallback behavior

Run:

```bash
pytest test_agent.py
```

## Common Issues

**Import errors**: make sure you are running commands from inside `week-8/examples/react-agent/`

**Tests not found**: install `pytest` with the provided `requirements.txt`

**Unknown location**: use one of the supported demo cities

## Next Steps

- add more tools
- replace rule-based routing with an LLM-backed planner
- log the full agent trace to a file
- expose the agent behind a FastAPI endpoint