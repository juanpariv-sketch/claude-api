from dotenv import load_dotenv
from anthropic import Anthropic
import json
import re
from pathlib import Path

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

def run_prompt(test_case):
    """Merges the prompt and test case input, then returns the result"""
    
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    
    messages = []
    add_user_message(messages, prompt)
    output = chat(messages)
    return output

def run_test_case(test_case):
    """Calls run_prompt, then grades the result"""
    output = run_prompt(test_case)
    
    # TODO - Grading
    score = 10
    
    return {
        "output": output,
        "test_case": test_case,
        "score": score
    }

def run_eval(dataset):
    """Loads the dataset and calls run_test_case with each case"""
    results = []
    
    for test_case in dataset:
        result = run_test_case(test_case)
        results.append(result)
    
    return results

dataset_path = Path(__file__).resolve().parent / "dataset.json"
with dataset_path.open("r", encoding="utf-8") as f:
    dataset = json.load(f)

results = run_eval(dataset)

print(json.dumps(results, indent=2))
