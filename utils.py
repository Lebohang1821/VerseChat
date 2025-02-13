import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv
from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
    ChatPromptTemplate
)

# Load environment variables
load_dotenv()

def load_chat_history():
    chat_history_str = os.getenv("CHAT_HISTORY", "[]")
    return json.loads(chat_history_str)

def save_chat_history(chat_history):
    os.environ["CHAT_HISTORY"] = json.dumps(chat_history)

def generate_ai_response(prompt_text, selected_model):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key is missing. Check your .env file.")

    url = f"https://generativelanguage.googleapis.com/v1/models/{selected_model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": prompt_text}]}]}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        response_json = response.json()
        try:
            return response_json["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Error: Unexpected response format."
    else:
        return f"Error: {response.status_code} - {response.text}"

def build_prompt():
    system_prompt = SystemMessagePromptTemplate.from_template(
        "You are a versatile AI assistant. You can help with a wide variety of topics including coding, general knowledge, science, entertainment, and more."
    )
    prompt_sequence = [system_prompt]
    message_log_str = os.getenv("CHAT_HISTORY", "[]")
    message_log = json.loads(message_log_str)
    for msg in message_log:
        if msg["role"] == "user":
            prompt_sequence.append(HumanMessagePromptTemplate.from_template(msg["content"]))
        elif msg["role"] == "ai":
            prompt_sequence.append(AIMessagePromptTemplate.from_template(msg["content"]))
    return ChatPromptTemplate.from_messages(prompt_sequence).format()
