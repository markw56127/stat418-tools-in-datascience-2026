from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field
from typing import Any

from llm_client import LLMClientError, chat_completion
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SYSTEM_PROMPT = """You are an assistant that can use MCP tools exposed by an external server.
Use the available tools when they help answer the user accurately.
Do not invent tool outputs.
After tool results are available, produce a concise final answer.
"""


@dataclass
class MCPToolCall:
    tool_name: str
    arguments: dict[str, Any]
    result: Any


@dataclass
class MCPAgentResult:
    final_answer: str
    tool_calls: list[MCPToolCall] = field(default_factory=list)


class MCPReActAgent:
    def __init__(self, max_turns: int = 5) -> None:
        self.max_turns = max_turns

    async def run(self, task: str) -> MCPAgentResult:
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server.py"],
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools_result = await session.list_tools()
                llm_tools = [self._tool_to_openrouter_schema(tool) for tool in tools_result.tools]

                messages: list[dict[str, Any]] = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": task},
                ]
                tool_calls: list[MCPToolCall] = []

                for _ in range(self.max_turns):
                    assistant_message = chat_completion(
                        messages=messages,
                        tools=llm_tools,
                        tool_choice="auto",
                        temperature=0.0,
                    )

                    raw_content = assistant_message.get("content")
                    raw_tool_calls = assistant_message.get("tool_calls", [])

                    messages.append(
                        {
                            "role": "assistant",
                            "content": raw_content or "",
                            **({"tool_calls": raw_tool_calls} if raw_tool_calls else {}),
                        }
                    )

                    if not raw_tool_calls:
                        final_answer = self._extract_text_content(raw_content)
                        return MCPAgentResult(final_answer=final_answer, tool_calls=tool_calls)

                    for tool_call in raw_tool_calls:
                        function_data = tool_call["function"]
                        tool_name = function_data["name"]
                        arguments = json.loads(function_data.get("arguments", "{}"))

                        tool_result = await session.call_tool(tool_name, arguments=arguments)
                        normalized_result = self._normalize_tool_result(tool_result)

                        tool_calls.append(
                            MCPToolCall(
                                tool_name=tool_name,
                                arguments=arguments,
                                result=normalized_result,
                            )
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call["id"],
                                "content": json.dumps(normalized_result),
                            }
                        )

                raise RuntimeError("Agent exceeded max_turns without producing a final answer.")

    @staticmethod
    def _tool_to_openrouter_schema(tool: Any) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description or "",
                "parameters": tool.inputSchema,
            },
        }

    @staticmethod
    def _normalize_tool_result(result: Any) -> Any:
        if hasattr(result, "content"):
            normalized_content = []
            for item in result.content:
                if hasattr(item, "text"):
                    normalized_content.append(item.text)
                else:
                    normalized_content.append(str(item))
            if len(normalized_content) == 1:
                try:
                    return json.loads(normalized_content[0])
                except json.JSONDecodeError:
                    return normalized_content[0]
            return normalized_content
        return str(result)

    @staticmethod
    def _extract_text_content(content: Any) -> str:
        if content is None:
            return ""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(item.get("text", ""))
            return "\n".join(part for part in parts if part).strip()
        return str(content)


if __name__ == "__main__":
    agent = MCPReActAgent()
    try:
        result = asyncio.run(agent.run("Look up alice, summarize her account, and send her a notification."))
        print(result.final_answer)
        for call in result.tool_calls:
            print(f"{call.tool_name}: {call.arguments} -> {call.result}")
    except LLMClientError as exc:
        print(f"LLM configuration error: {exc}")


