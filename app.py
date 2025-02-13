from flask import Flask, request, jsonify, render_template
from utils import load_chat_history, save_chat_history, generate_ai_response, build_prompt
import logging
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load chat history
chat_history = load_chat_history()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verse_of_the_day')
def verse_of_the_day():
    return render_template('verse_of_the_day.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_query = request.json['message']
        selected_model = "gemini-1.5-pro"  # Default model, you can change this as needed
        
        # Add user message to log
        chat_history.append({"role": "user", "content": user_query})
        save_chat_history(chat_history)
        
        # Generate AI response
        prompt_text = build_prompt()
        ai_response = generate_ai_response(prompt_text, selected_model)
        
        # Add AI response to log
        chat_history.append({"role": "ai", "content": ai_response})
        
        # Save chat to history
        save_chat_history(chat_history)
        
        logging.debug(f"AI response: {ai_response}")
        return jsonify({"response": ai_response})
    except Exception as e:
        logging.error(f"Error in /chat endpoint: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
