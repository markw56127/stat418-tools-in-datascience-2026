# MCP-Powered Agent

A runnable example of an LLM agent using a real FastMCP server, the Python MCP client library, and OpenRouter tool-calling.

## Overview

This example demonstrates:
- defining tools with FastMCP
- exposing those tools through a real MCP server over stdio
- discovering tools dynamically with the Python `mcp` client library
- using OpenRouter with a Gemini model for tool selection and final answer generation
- combining local tools and external APIs in an MCP workflow

## Files

- `mcp_server.py` - FastMCP server that exposes demo tools
- `mcp_agent.py` - LLM-driven MCP client agent using `ClientSession`
- `llm_client.py` - OpenRouter chat completion helper
- `config.json` - example MCP client configuration
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

## Running the MCP Server

You can run the FastMCP server directly:

```bash
python mcp_server.py
```

The server exposes these tools:
- `search_database`
- `get_user_info`
- `get_weather`
- `send_notification`

## Running the Agent

The agent launches the MCP server over stdio, initializes an MCP session, discovers the available tools, and lets the LLM decide when to call them.

```bash
python mcp_agent.py
```

The default task in `mcp_agent.py`:
- looks up `alice`
- summarizes her account
- sends a notification

You can adapt the task string in the script to ask for:
- weather for a user's city
- product recommendations
- user lookup plus follow-up actions

## Config File

`config.json` shows the same server registration pattern many MCP hosts use:

```json
{
  "mcpServers": {
    "demo-tools": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "."
    }
  }
}
```

## FastMCP Server Design

The server uses the `@mcp.tool` decorator to publish discoverable tool interfaces:

```python
from fastmcp import FastMCP

mcp = FastMCP("demo-tools")

@mcp.tool
def get_user_info(username: str) -> dict:
    ...
```

The tool layer includes:
- a small in-memory product database
- demo user account data
- live weather lookup through Open-Meteo
- a notification action that returns structured delivery metadata

## MCP Client Design

The agent uses the actual Python MCP client library:

- `StdioServerParameters`
- `stdio_client(...)`
- `ClientSession(...)`
- `session.initialize()`
- `session.list_tools()`
- `session.call_tool(...)`

That means the example is not pretending to be MCP-compatible. It is using the real protocol client flow.

## Example Workflow

A representative multi-step request is:

```text
Look up alice, check the weather in her city, and send her a short notification.
```

A typical execution path is:
1. the LLM sees the available MCP tool schemas
2. it calls `get_user_info`
3. it calls `get_weather` with the returned city
4. it calls `send_notification`
5. it produces a final answer summarizing the completed workflow

## Why This Example Is Better Than the Earlier Version

This version now includes:
- a real external LLM API
- actual tool-calling
- a real MCP client session
- a real MCP server
- a real external weather API

That makes it much closer to how production agent systems are structured.

## Common Issues

**`fastmcp` or `mcp` import error**: install dependencies with `uv pip install -r requirements.txt`

**`OPENROUTER_API_KEY is not set`**: export the environment variable before running the agent

**Unknown user**: use `alice` or `bob` in demo prompts unless you extend `USERS`

**Weather lookup failed**: the Open-Meteo geocoding request may fail if the city is misspelled or the network is unavailable

**Server/client confusion**: `mcp_server.py` defines the tools and can be run directly, but `mcp_agent.py` also starts that server internally over stdio for the MCP session

