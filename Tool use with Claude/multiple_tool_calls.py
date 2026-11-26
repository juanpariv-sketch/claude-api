from dotenv import load_dotenv
from anthropic import Anthropic
import json
from datetime import datetime

load_dotenv()

client = Anthropic()
model = "claude-haiku-5-5"

# Helper functions
from anthropic.types import Message
def add_user_message(messages, message):
    user_message = {
        "role": "user",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(user_message)

def add_assistant_message(messages, message):
    assistant_message = {
        "role": "assistant",
        "content": message.content if isinstance(message, Message) else message
    }
    messages.append(assistant_message)


def chat(messages, system=None, tools=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }

    if system:
        params["system"] = system

    if tools:
        params["tools"] = tools

    response = client.messages.create(**params)

    return response

def text_from_message(message):
    return "\n".join(
        [block.text for block in message.content if block.type == "text"]
    )

def run_tool(tool_name, tool_input):
    if tool_name == "get_current_date_time":
        return get_current_date_time(**tool_input)

def run_tools(message):
    tool_requests = [
        block for block in message.content if block.type == "tool_use"
    ]

    tool_result_blocks = []

    for tool_request in tool_requests:
        try:
            tool_output = run_tool(tool_request.name, tool_request.input)
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": json.dumps(tool_output),
                "is_error": False,
            }

        except Exception as e:
            tool_result_block = {
                "type": "tool_result",
                "tool_use_id": tool_request.id,
                "content": f"Error: {e}",
                "is_error": True,
            }

        tool_result_blocks.append(tool_result_block)

    return tool_result_blocks
 
def run_conversation(messages):
    while True:
        response = chat(messages, tools=[get_current_date_time_schema])
        add_assistant_message(messages, response)
        print(text_from_message(response))

        if response.stop_reason != "tool_use":
            break

        tool_results = run_tools(response)
        add_user_message(messages, tool_results)

    return messages

# Tools and Schemas
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

# Example usage
messages = []
add_user_message(messages, "What is the exact time right now, formatted as HH:MM?, Also, what is the current time in SS format?")

run_conversation(messages)
print(messages)