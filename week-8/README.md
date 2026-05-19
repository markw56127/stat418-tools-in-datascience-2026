# Week 8: AI Agents & Advanced MCP Integration

## Overview

This week focuses on two concrete agent implementations that you can run locally:

1. a **Simple ReAct Agent** in `examples/react-agent/`
2. an **MCP-Powered Agent** in `examples/mcp-agent/`

Instead of treating agents as only abstract concepts, the week is organized around these two runnable examples. The ReAct example introduces the basic thought-action-observation loop. The MCP example shows how tools can be exposed through a FastMCP server and used in a more structured tool ecosystem.

## How to Use This Week

Work through the materials in this order:

1. Read the ReAct example in `examples/react-agent/`
2. Run `agent.py` and inspect `tools.py`
3. Run the ReAct tests in `test_agent.py`
4. Move to `examples/mcp-agent/`
5. Run the FastMCP server in `mcp_server.py`
6. Run the MCP agent in `mcp_agent.py`
7. Compare how direct local tools differ from MCP-exposed tools

## Topics Covered

### 1. AI Agent Fundamentals
Grounded in `examples/react-agent/`

- what an AI agent is
- the thought → action → observation loop
- tool use and function schemas
- fallback behavior when no tool applies
- basic agent testing

### 2. ReAct Agent Design
Grounded in `examples/react-agent/agent.py`

- implementing a simple ReAct loop
- routing tasks to tools
- generating a final answer from tool output
- tracing agent behavior step by step

### 3. Tool Design
Grounded in `examples/react-agent/tools.py`

- defining focused tool functions
- attaching lightweight schemas to tools
- returning structured outputs
- keeping tools small and teachable

### 4. MCP Integration Patterns
Grounded in `examples/mcp-agent/`

- exposing tools through FastMCP
- server-side tool registration
- discoverable tool interfaces
- agent interaction with MCP-style tools

### 5. FastMCP Server Design
Grounded in `examples/mcp-agent/mcp_server.py`

- creating an MCP server with `FastMCP`
- decorating functions as tools
- designing useful tool signatures
- organizing a simple local MCP workflow

### 6. MCP Agent Workflows
Grounded in `examples/mcp-agent/mcp_agent.py`

- selecting which MCP-style tool to use
- looking up demo users
- sending demo notifications
- querying a small demo product database

### 7. Testing and Reliability
Grounded in `examples/react-agent/test_agent.py`

- testing expected agent behavior
- checking tool routing
- checking fallback logic
- building confidence in agent examples before adding LLMs

## Why This Matters

AI agents are useful because they can:
- reason about tasks
- call tools
- use observations to decide what to do next
- complete multi-step workflows instead of only producing text

For this course, the key idea is not just that agents are powerful, but that you can build and inspect them as ordinary Python programs.

## Example 1: Simple ReAct Agent

Location:
- `week-8/examples/react-agent/`

Files:
- `agent.py`
- `tools.py`
- `test_agent.py`
- `requirements.txt`

What it demonstrates:
- a direct local ReAct loop
- a weather tool
- a simple product search tool
- deterministic behavior that is easy to inspect
- tests that verify expected outcomes

Run it:

```bash
cd week-8/examples/react-agent
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python agent.py
pytest test_agent.py
```

## Example 2: MCP-Powered Agent

Location:
- `week-8/examples/mcp-agent/`

Files:
- `mcp_server.py`
- `mcp_agent.py`
- `config.json`
- `requirements.txt`

What it demonstrates:
- tools defined with FastMCP
- a simple local MCP server
- discoverable tool endpoints
- a matching Python agent workflow
- a configuration file for local MCP registration

Run it:

```bash
cd week-8/examples/mcp-agent
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python mcp_server.py
```

In a separate terminal:

```bash
cd week-8/examples/mcp-agent
source .venv/bin/activate
python mcp_agent.py
```

## Key Concept: The Agent Loop

The ReAct example shows this loop directly:

1. receive a task
2. decide which tool to use
3. call the tool
4. inspect the result
5. produce a final answer

This is the simplest useful mental model for agents.

## Key Concept: MCP

The MCP example shows a more structured pattern:

```text
Agent → MCP Server → Tool Functions
```

This matters because:
- tools become discoverable
- tool interfaces become more standardized
- assistants and applications can share tool servers
- the agent and the tool implementation are more clearly separated

## Comparing the Two Examples

### ReAct example
Best for:
- introducing the core loop
- understanding local tool calling
- testing agent logic
- showing step-by-step reasoning

### MCP example
Best for:
- showing tool servers
- explaining discoverable tools
- connecting agents to structured tool ecosystems
- demonstrating how agent systems scale beyond direct local function calls

## Suggested Teaching Flow

1. Start with `examples/react-agent/agent.py`
2. Open `examples/react-agent/tools.py`
3. Show the weather and database tools
4. Run the agent and inspect the printed steps
5. Run the tests
6. Transition to `examples/mcp-agent/mcp_server.py`
7. Show the `@mcp.tool` decorators
8. Run the MCP server
9. Run the MCP agent
10. Compare direct tools versus MCP tools

## Best Practices

### Agent Design
- start with simple loops
- make tool use observable
- keep actions deterministic early on
- add complexity gradually

### Tool Design
- keep tools single-purpose
- provide clear inputs and outputs
- validate assumptions
- return structured results

### Testing
- test simple scenarios first
- test fallback behavior
- verify tools independently
- avoid adding LLM complexity before the basic workflow is correct

## Common Pitfalls

- over-engineering too early
- hiding the agent loop behind too much framework code
- making tools too broad or unclear
- skipping tests
- mixing abstract agent concepts with no runnable example

## Resources

### ReAct and agent design
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)

### MCP
- [MCP Specification](https://modelcontextprotocol.io/)
- [Building MCP Servers](https://modelcontextprotocol.io/docs/building-servers)

### Python tooling
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Pytest Documentation](https://docs.pytest.org/)

## Week 8 Summary

By the end of this week, students should be able to:

- explain the ReAct loop
- build a simple local tool-using agent
- test agent behavior
- expose tools with FastMCP
- explain the difference between local tool calling and MCP-based tool serving
- use the provided examples as a base for more advanced agent systems
