from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()
model = "claude-haiku-5-5"

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
    
    message = client.messages.create(**params)
    return message.content[0].text

# Start with an empty message list
messages = []
system_prompt = """
You are a helpful assistant that provides concise and clear explanations. 
Please answer the user's questions in a brief manner, 
focusing on the key points without unnecessary details.
"""

# Add the initial user question
question_1="Explain the CI/CD process"
add_user_message(messages, question_1)
print("User: ", question_1)

# Get Claude's response
answer = chat(messages, system=system_prompt)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)
print("Assistant:", answer)