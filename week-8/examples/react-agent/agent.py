from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from tools import TOOLS


@dataclass
class Step:
    thought: str
    action: str | None = None
    action_input: dict[str, Any] | None = None
    observation: Any | None = None


@dataclass
class AgentResult:
    final_answer: str
    steps: list[Step] = field(default_factory=list)


class ReActAgent:
    def __init__(self, max_turns: int = 5) -> None:
        self.max_turns = max_turns
        self.retry_count = 0

    def call_tool(self, tool_name: str, args: dict[str, Any]) -> Any:
        if tool_name not in TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")
        return TOOLS[tool_name](**args)

    def run(self, task: str) -> AgentResult:
        task_lower = task.lower()
        steps: list[Step] = []

        if "weather" in task_lower:
            location = self._extract_location(task)
            thought = f"I need to get the weather for {location}."
            observation = self.call_tool("get_weather", {"location": location})
            steps.append(
                Step(
                    thought=thought,
                    action="get_weather",
                    action_input={"location": location},
                    observation=observation,
                )
            )

            rain = observation["precipitation_chance"]
            if rain >= 50:
                recommendation = "You should bring an umbrella."
            else:
                recommendation = "You probably do not need an umbrella."

            final_answer = (
                f"The weather in {location} is {observation['temp_f']}°F and "
                f"{observation['conditions']} with a {rain}% chance of rain. "
                f"{recommendation}"
            )
            return AgentResult(final_answer=final_answer, steps=steps)

        if "search" in task_lower or "database" in task_lower or "laptop" in task_lower:
            query = self._extract_query(task)
            thought = f"I should search the product database for '{query}'."
            observation = self.call_tool("search_database", {"query": query})
            steps.append(
                Step(
                    thought=thought,
                    action="search_database",
                    action_input={"query": query},
                    observation=observation,
                )
            )

            if not observation:
                final_answer = f"No products matched '{query}'."
            else:
                products = ", ".join(product["name"] for product in observation)
                final_answer = f"I found these matching products: {products}."
            return AgentResult(final_answer=final_answer, steps=steps)

        steps.append(
            Step(
                thought="I do not have an appropriate tool for this task, so I should respond directly."
            )
        )
        return AgentResult(
            final_answer="I can currently help with weather questions and simple product database searches.",
            steps=steps,
        )

    @staticmethod
    def _extract_location(task: str) -> str:
        known_locations = ["San Francisco", "Los Angeles", "New York"]
        for location in known_locations:
            if location.lower() in task.lower():
                return location
        return "San Francisco"

    @staticmethod
    def _extract_query(task: str) -> str:
        for query in ["laptop", "audio", "keyboard", "accessory"]:
            if query in task.lower():
                return query
        return task.strip()


def print_result(result: AgentResult) -> None:
    for step in result.steps:
        print(f"Thought: {step.thought}")
        if step.action:
            print(f"Action: {step.action}({json.dumps(step.action_input)})")
        if step.observation is not None:
            print(f"Observation: {json.dumps(step.observation)}")
        print()
    print(f"Final Answer: {result.final_answer}")


if __name__ == "__main__":
    agent = ReActAgent()
    user_task = "What's the weather in San Francisco and should I bring an umbrella?"
    result = agent.run(user_task)
    print_result(result)

# Made with Bob
