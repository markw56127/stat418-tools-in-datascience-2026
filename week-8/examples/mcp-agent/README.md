# MCP-Powered Agent

A runnable example of an agent working with a FastMCP server and discoverable tools.

## Overview

This example demonstrates:
- defining tools with FastMCP
- exposing those tools through an MCP server
- using MCP-style tools from a Python agent
- simple user lookup, notification, and database search workflows
- local configuration for connecting a client to the server

## Files

- `mcp_server.py` - FastMCP server with demo tools
- `mcp_agent.py` - simple Python agent that uses the demo tools
- `config.json` - example MCP client configuration
- `requirements.txt` - Python dependencies

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

This example is local and self-contained so it can be demonstrated in class without external APIs.

## Running the MCP Server

```bash
python mcp_server.py
```

The server exposes these tools:
- `search_database`
- `get_user_info`
- `send_notification`

## Running the Agent

```bash
python mcp_agent.py
```

Example behavior:
- look up a demo user such as `alice`
- optionally send that user a mock notification
- search a tiny product database

## Config File

`config.json` provides a minimal example of how a local MCP client could register the server:

```json
{
  "mcpServers": {
    "demo-tools": {
      "command": "python",
      "args": ["mcp_server.py"]
    }
  }
}
```

## FastMCP Server Design

The server defines tools with the `@mcp.tool` decorator. This keeps the example simple and readable:

```python
from fastmcp import FastMCP

mcp = FastMCP("demo-tools")

@mcp.tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    ...
```

## Demo Workflows

### User lookup
The agent can retrieve information for:
- `alice`
- `bob`

### Notification sending
The agent can simulate sending a notification message to a known user.

### Product search
The agent can search a tiny in-memory product catalog for:
- laptops
- tablets

## Teaching Notes

This example is designed to support the week 8 topics:
- MCP server setup
- discoverable tools
- agent-to-tool interaction
- structured tool inputs and outputs

The agent is intentionally simple so students can focus on the MCP pattern before layering in LLM-based tool selection.

## Common Issues

**`fastmcp` import error**: install dependencies with `uv pip install -r requirements.txt`

**Unknown user**: use `alice` or `bob` in the demo task

**Server/client confusion**: `mcp_server.py` defines tools and runs the server; `mcp_agent.py` demonstrates how an agent would use those tools in a simple workflow

## Next Steps

- connect a real MCP client implementation
- add tests for the MCP example
- swap rule-based task routing for an LLM planner
- add more domain-specific tools