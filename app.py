from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

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
def get_gemini_response(message):
    url = "https://api.gemini.com/v1/chat"
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "message": message
    }
    logging.debug(f"Sending request to Gemini API: {data}")
    response = requests.post(url, headers=headers, json=data)
    logging.debug(f"Gemini API response: {response.status_code} - {response.text}")
    if response.status_code == 200:
        return response.json().get('response', "Sorry, I couldn't understand that.")
    else:
        return "Sorry, there was an error with the Gemini API."

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
