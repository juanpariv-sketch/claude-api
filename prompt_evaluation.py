# Load env variables and create client
from dotenv import load_dotenv
from anthropic import Anthropic
import json
import re

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
            
def generate_dataset():
    prompt = """
Generate a evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts
that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects,
each representing task that requires Python, JSON, or a Regex to complete.

Example output, in JSON format:

[
    {
        "task": "Description of task",
    },
    {
        "task": "Description of task",
    }
    ...additional
]


* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a regular expression.
* Focus on tasks that do not require writing much code

Please generate 3 objects.
"""
    messages = []
    add_user_message(messages, prompt)
    text = chat(messages)
    #print(text)
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL | re.IGNORECASE)
    if not re.match:
        raise ValueError("No JSON code block found")

    return json.loads(match.group(1))

dataset = generate_dataset()
print(dataset)