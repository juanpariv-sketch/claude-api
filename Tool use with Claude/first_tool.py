from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import datetime

load_dotenv()

client = Anthropic()
model = "claude-haiku-5-5"

# Helper functions
def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)


def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)


def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    response = client.messages.create(**params)
    #print(response)

    for block in response.content:
        if block.type == "text":
            return block.text

from anthropic.types import ToolParam

def get_current_date_time(date_format="%Y-%m-%d %H:%M:%S"):
    """Returns the current date and time in the specified format."""
    if not date_format:
        raise ValueError("Date format cannot be empty")
    return datetime.now().strftime(date_format)

get_current_date_time_schema = ToolParam({
    "name": "get_current_date_time",
    "description": "Get the current date and time in the specified format.",
    "input_schema": {
        "type": "object",
        "properties": {
            "date_format": {
                "type": "string",
                "description": "The format in which to return the current date and time, using Python's strftime directives. For example, '%Y-%m-%d %H:%M:%S' for '2025-04-03 10:30:00'.",
                "default": "%Y-%m-%d %H:%M:%S"
            }
        },
        "required": []
    }
})

messages = []
messages.append(
    {
        "role": "user",
        "content": "What is the exact time right now, formatted as HH:MM:SS?"
    }
)

response = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_date_time_schema],
)

messages.append({
    "role": "assistant",
    "content": response.content
})

#print(response)
#print(messages)


result = get_current_date_time(**response.content[0].input)
#print(result)

messages.append({
    "role": "user",
    "content": [
        {
            "type": "tool_result",
            "tool_use_id": response.content[0].id,
            "content": result,
            "is_error": False
        }
    ] 
})

response2 = client.messages.create(
    model=model,
    max_tokens=1000,
    messages=messages,
    tools=[get_current_date_time_schema],
)

print(response2)