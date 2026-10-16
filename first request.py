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

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text

# Start with an empty message list
messages = []

# Add the initial user question
question_1="Explain the CI/CD process very briefly"
add_user_message(messages, question_1)
print("User: ", question_1)

# Get Claude's response
answer = chat(messages)

# Add Claude's response to the conversation history
add_assistant_message(messages, answer)
print("Assistant:", answer)

# Add a follow-up question
follow_up_question = "Briefly, what does a Devops Engineer do in the CI/CD process?"
add_user_message(messages, follow_up_question)
print("User: ", follow_up_question)

# Get the follow-up response with full context
final_answer = chat(messages)
print("Assistant:", final_answer)