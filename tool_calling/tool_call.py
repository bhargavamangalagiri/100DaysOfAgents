# Our small, fictional ticket database.
tickets = {
    "T-101": {
        "title": "Cannot log in",
        "status": "open",
        "priority": "high",
    },
    "T-102": {
        "title": "Invoice missing",
        "status": "resolved",
        "priority": "low",
    },
}


# This ordinary Python function will become an agent's tool.
def get_ticket(ticket_id: str) -> dict:
    if ticket_id not in tickets:
        return {"error": f"Ticket {ticket_id} not found"}

    return tickets[ticket_id]


# Call the function ourselves before introducing a model.
tool_call = {
    "name": "get_ticket",
    "arguments": {
        "ticket_id": "T-102",
    },
}

available_tools = {
    "get_ticket": get_ticket,
}

def execute_tool(tool_call: dict) -> dict:
    tool_name = tool_call["name"]
    arguments = tool_call["arguments"]

    if tool_name not in available_tools:
        return {"error": f"Unknown tool: {tool_name}"}

    if not isinstance(arguments, dict):
        return {"error": "arguments must be a dictionary"}

    if set(arguments) != {"ticket_id"}:
        return {"error": "Arguments must contain only ticket_id"}

    if not isinstance(arguments["ticket_id"], str):
        return {"error": "ticket_id must be a string"}

    tool_function = available_tools[tool_name]
    return tool_function(**arguments)


tool_name = tool_call["name"]
arguments = tool_call["arguments"]

result = execute_tool(tool_call)

test_cases = [
    (
        "Existing ticket",
        {
            "name": "get_ticket",
            "arguments": {"ticket_id": "T-102"},
        },
        {
            "title": "Invoice missing",
            "status": "resolved",
            "priority": "low",
        },
    ),
    (
        "Unknown tool",
        {
            "name": "delete_ticket",
            "arguments": {"ticket_id": "T-102"},
        },
        {"error": "Unknown tool: delete_ticket"},
    ),
    (
        "Incorrect argument type",
        {
            "name": "get_ticket",
            "arguments": {"ticket_id": 102},
        },
        {"error": "ticket_id must be a string"},
    ),
]

if __name__ == "__main__":
    for label, request, expected in test_cases:
        actual = execute_tool(request)
        assert actual == expected, f"{label}: got {actual}"
        print(f"PASS: {label}")
