from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from mcp_server import get_user_info, search_database, send_notification


@dataclass
class MCPToolCall:
    tool_name: str
    arguments: dict[str, Any]
    result: Any


@dataclass
class MCPAgentResult:
    final_answer: str
    tool_calls: list[MCPToolCall] = field(default_factory=list)


class DemoMCPAgent:
    def run(self, task: str) -> MCPAgentResult:
        task_lower = task.lower()
        tool_calls: list[MCPToolCall] = []

        if "alice" in task_lower or "bob" in task_lower:
            username = "alice" if "alice" in task_lower else "bob"
            user_info = get_user_info(username)
            tool_calls.append(
                MCPToolCall(
                    tool_name="get_user_info",
                    arguments={"username": username},
                    result=user_info,
                )
            )

            if "notify" in task_lower or "notification" in task_lower:
                message = f"Hello {user_info['name']}, this is your demo MCP notification."
                notification = send_notification(username, message)
                tool_calls.append(
                    MCPToolCall(
                        tool_name="send_notification",
                        arguments={"username": username, "message": message},
                        result=notification,
                    )
                )
                final_answer = (
                    f"Found user {user_info['name']} on the {user_info['plan']} plan and "
                    f"sent a notification to {user_info['email']}."
                )
                return MCPAgentResult(final_answer=final_answer, tool_calls=tool_calls)

            final_answer = (
                f"Found user {user_info['name']} with the {user_info['plan']} plan and "
                f"email {user_info['email']}."
            )
            return MCPAgentResult(final_answer=final_answer, tool_calls=tool_calls)

        if "laptop" in task_lower or "tablet" in task_lower or "database" in task_lower:
            query = "laptop" if "laptop" in task_lower else "tablet"
            results = search_database(query=query, limit=5)
            tool_calls.append(
                MCPToolCall(
                    tool_name="search_database",
                    arguments={"query": query, "limit": 5},
                    result=results,
                )
            )
            final_answer = f"Found {len(results)} matching products for '{query}'."
            return MCPAgentResult(final_answer=final_answer, tool_calls=tool_calls)

        return MCPAgentResult(
            final_answer=(
                "I can currently query demo users, send demo notifications, "
                "and search the demo product database."
            ),
            tool_calls=tool_calls,
        )


if __name__ == "__main__":
    agent = DemoMCPAgent()
    result = agent.run("Look up alice and send her a notification.")
    print(result.final_answer)
    for call in result.tool_calls:
        print(f"{call.tool_name}: {call.arguments} -> {call.result}")

# Made with Bob
