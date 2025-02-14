import os
import json
import requests
import logging
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

    # Fetch a random Bible verse
    try:
        bible_response = requests.get("https://bible-api.com/")
        bible_response.raise_for_status()
        bible_data = bible_response.json()
        bible_verse = bible_data["text"]
    except requests.RequestException as e:
        logging.error(f"Error fetching Bible verse: {e}", exc_info=True)
        bible_verse = "Error: Unable to fetch Bible verse."

    url = f"https://generativelanguage.googleapis.com/v1/models/{selected_model}:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": f"{prompt_text}\n\nBible Verse: {bible_verse}\n\nMotivational Message: Keep faith and stay strong!"}]}]}

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        response_json = response.json()
        try:
            ai_response = response_json["candidates"][0]["content"]["parts"][0]["text"]
            # Handle responses containing "****"
            if "****" in ai_response:
                ai_response = ai_response.replace("****", "[censored]")
            # Ensure proper encoding
            ai_response = ai_response.encode('utf-8', 'ignore').decode('utf-8')
            return ai_response
        except (KeyError, IndexError) as e:
            logging.error(f"Error parsing AI response: {e}", exc_info=True)
            return "Error: Unexpected response format."
    except requests.RequestException as e:
        logging.error(f"Error generating AI response: {e}", exc_info=True)
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
