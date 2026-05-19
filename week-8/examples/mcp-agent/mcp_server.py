from __future__ import annotations

from fastmcp import FastMCP


mcp = FastMCP("demo-tools")

PRODUCTS = [
    {"id": 1, "name": "Laptop Pro 14", "category": "laptop", "price": 1499},
    {"id": 2, "name": "Notebook Air 13", "category": "laptop", "price": 999},
    {"id": 3, "name": "Study Tablet", "category": "tablet", "price": 599},
]

USERS = {
    "alice": {"name": "Alice", "plan": "premium", "email": "alice@example.com"},
    "bob": {"name": "Bob", "plan": "free", "email": "bob@example.com"},
}


@mcp.tool
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search a tiny in-memory product database."""
    normalized = query.strip().lower()
    return [
        product
        for product in PRODUCTS
        if normalized in product["name"].lower() or normalized in product["category"].lower()
    ][:limit]


@mcp.tool
def get_user_info(username: str) -> dict:
    """Get information about a known demo user."""
    normalized = username.strip().lower()
    if normalized not in USERS:
        raise ValueError(f"Unknown user: {username}")
    return USERS[normalized]


@mcp.tool
def send_notification(username: str, message: str) -> dict:
    """Simulate sending a notification."""
    return {
        "status": "sent",
        "username": username,
        "message": message,
    }


if __name__ == "__main__":
    mcp.run()

# Made with Bob
