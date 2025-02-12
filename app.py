from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging
import json

# Load environment variables from .env file (do this EARLY)
load_dotenv()

app = Flask(__name__)

# Access environment variables SAFELY
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Check if required environment variables are set
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY must be set in .env")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to get Bible verse
def get_bible_verse(book, chapter, verse):
    url = f"https://bible-api.com/{book}%20{chapter}:{verse}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['text']
    else:
        return "Sorry, we couldn't find that verse. Please try again."

# Function to interact with Gemini API
def get_gemini_response(message, selected_model="gemini-1.5-pro"):
    api_key = GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1/models/{selected_model}:generateContent?key={api_key}"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "instances": [
            {
                "messages": [{"author": "user", "content": message}]
            }
        ],
        "parameters": {}
    }
    logging.debug(f"Sending request to Gemini API: {json.dumps(data, indent=2)}")

    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)  # Add a timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        response_json = response.json()
        predictions = response_json.get('predictions', [])
        if predictions:
            candidates = predictions[0].get('candidates', [])
            if candidates:
                text = candidates[0].get('text')
                return text
        return "No response from Gemini"
    except requests.exceptions.RequestException as e:
        logging.error(f"Error communicating with Gemini API: {e}")
        return f"Error with Gemini API: {e}"  # Return the error message
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        logging.error(f"Error parsing Gemini response: {e}")
        return "Error processing Gemini response"

@app.route('/', methods=['GET', 'POST'])
def index():
    verse_text = ""
    if request.method == 'POST':
        book = request.form['book']
        chapter = request.form['chapter']
        verse = request.form['verse']
        verse_text = get_bible_verse(book, chapter, verse)
    return render_template('index.html', verse_text=verse_text)

@app.route('/api/get_verse', methods=['GET'])
def api_get_verse():
    book = request.args.get('book')
    chapter = request.args.get('chapter')
    verse = request.args.get('verse')
    if book and chapter and verse:
        verse_text = get_bible_verse(book, chapter, verse)
        return jsonify({"verse_text": verse_text})
    else:
        return jsonify({"error": "Missing parameters"}), 400

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_message = request.json.get('message')
    if user_message:
        gemini_response = get_gemini_response(user_message)
        return jsonify({"response": gemini_response})
    else:
        return jsonify({"error": "No message provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
