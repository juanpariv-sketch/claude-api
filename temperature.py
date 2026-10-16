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

def chat(messages, system=None, temperature=1.0):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    return message.content[0].text

# Start with an empty message list
messages = []

# Add the initial user question
question_1="Explain the CI/CD process"
add_user_message(messages, question_1)
print("User: ", question_1)

# Get Claude's response
answer = chat(messages, temperature=0)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)
print("Assistant:", answer)