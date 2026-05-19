from __future__ import annotations

from typing import Any


WEATHER_DATA = {
    "san francisco": {
        "temp_f": 65,
        "conditions": "partly cloudy",
        "precipitation_chance": 20,
    },
    "los angeles": {
        "temp_f": 74,
        "conditions": "sunny",
        "precipitation_chance": 5,
    },
    "new york": {
        "temp_f": 59,
        "conditions": "light rain",
        "precipitation_chance": 75,
    },
}

PRODUCTS = [
    {"name": "Laptop Pro 14", "category": "laptop", "price": 1499},
    {"name": "Notebook Air 13", "category": "laptop", "price": 999},
    {"name": "Noise Canceling Headphones", "category": "audio", "price": 299},
    {"name": "Mechanical Keyboard", "category": "accessory", "price": 129},
]


def get_weather(location: str) -> dict[str, Any]:
    """Return mock weather data for a supported location."""
    normalized = location.strip().lower()
    if normalized not in WEATHER_DATA:
        raise ValueError(f"Unknown location: {location}")
    return {"location": location, **WEATHER_DATA[normalized]}


def search_database(query: str) -> list[dict[str, Any]]:
    """Search a tiny in-memory product catalog."""
    normalized = query.strip().lower()
    return [
        product
        for product in PRODUCTS
        if normalized in product["name"].lower() or normalized in product["category"].lower()
    ]


TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "search_database",
        "description": "Search a small product database.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search term"},
            },
            "required": ["query"],
        },
    },
]


TOOLS = {
    "get_weather": get_weather,
    "search_database": search_database,
}

# Made with Bob
