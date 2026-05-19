# Simple ReAct Agent

A runnable implementation of a ReAct-style agent using a real LLM API, OpenRouter tool-calling, and a live weather tool backed by Open-Meteo.

## Overview

This example demonstrates:
- a ReAct-style tool loop driven by a real LLM
- function/tool calling through OpenRouter
- a Gemini model selected through OpenRouter
- live weather lookup through Open-Meteo
- local product search with structured tool schemas
- lightweight tests around the non-network helper logic

## Files

- `agent.py` - main ReAct agent implementation
- `tools.py` - tool definitions and implementations
- `llm_client.py` - OpenRouter chat completion helper
- `test_agent.py` - unit tests for helper behavior
- `requirements.txt` - Python dependencies

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Set your OpenRouter API key before running the agent:

```bash
export OPENROUTER_API_KEY=your_key_here
```

Optional model override:

```bash
export OPENROUTER_MODEL=google/gemini-2.0-flash-001
```

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

Tool Call: get_weather({"location": "San Francisco"})
Tool Result: {"location": "San Francisco", "temp_f": 58.4, "conditions": "partly cloudy", "wind_speed_mph": 7.1}

Final Answer: San Francisco is currently cool and partly cloudy. Based on the current conditions, bringing a light jacket makes sense, but an umbrella may not be necessary unless you expect conditions to change later.
```

## Supported Tools

### `get_weather`
Looks up live weather data using Open-Meteo:
- geocodes the requested city
- fetches the current forecast
- returns structured weather fields

### `search_database`
Searches a tiny in-memory product catalog for:
- laptops
- tablets
- phones

## Key Concepts

### ReAct-Style Tool Loop

The agent follows this pattern:
1. send the user request and tool schemas to the model
2. let the model decide whether to call a tool
3. execute the requested tool locally
4. append the tool result to the conversation
5. ask the model for the final answer or next tool call

### Tool Definitions

Tools are represented in `tools.py` with:
- Python functions
- OpenAI/OpenRouter-compatible function schemas

This lets the same tool definitions work naturally with LLM tool-calling APIs.

## Extending the Agent

Add new tools by:
1. creating a new function in `tools.py`
2. adding a schema entry to the tool list
3. registering the function in the tool dispatch map
4. letting the LLM decide when to use it

## Testing

The current test file focuses on deterministic helper logic such as:
- extracting text from model responses
- handling unknown tools
- failing cleanly when the API key is missing

Run:

```bash
pytest test_agent.py
```

## Common Issues

**`OPENROUTER_API_KEY is not set`**: export the environment variable before running the agent

**Network/API errors**: both OpenRouter and Open-Meteo require network access

**Import errors**: make sure you are running commands from inside `week-8/examples/react-agent/`

**Unexpected tool behavior**: inspect the tool schemas and the exact JSON arguments returned by the model

