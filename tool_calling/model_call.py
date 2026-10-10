import json
import requests
import os
from tool_call import execute_tool

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is missing from this process's environment."
    )

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_ticket",
            "description": "Look up a support ticket by its ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {
                        "type": "string",
                        "description": "The ticket ID, for example T-102.",
                    }
                },
                "required": ["ticket_id"],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "What is the status of ticket T-102?",
    }
]

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {api_key}",
    },
    json={
        "model": "nvidia/nemotron-3-super-120b-a12b:free",
        "messages": messages,
        "tools": tools,
    },
    timeout=60,
)

response.raise_for_status()
data = response.json()
message = data["choices"][0]["message"]
tool_calls = message.get("tool_calls")

if tool_calls:
    messages.append(message)

    for call in tool_calls:
        tool_request = {
            "name": call["function"]["name"],
            "arguments": json.loads(call["function"]["arguments"]),
        }

        result = execute_tool(tool_request)

        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": json.dumps(result),
        })

    final_response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
        },
        json={
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": messages,
        },
        timeout=60,
    )

    final_response.raise_for_status()
    final_data = final_response.json()
    print(final_data["choices"][0]["message"]["content"])

else:
    print(message.get("content"))