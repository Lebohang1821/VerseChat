# VerseChat

VerseChat is a simple web application that fetches and displays Bible verses using a graphical user interface..

## Prerequisites

Make sure you have Python installed on your system. You will also need the `requests`, `flask`, and `python-dotenv` libraries. You can install them using pip:

```sh
pip install -r requirements.txt
```

## Setup

1. Create a `.env` file in the `/f:/Work/VerseChat` directory and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

## How to Run

1. Save the code in a file named `app.py` inside the `/f:/Work/VerseChat` directory.
2. Create a `templates` directory inside `/f:/Work/VerseChat` and save the HTML file as `index.html`.
3. Open a terminal and navigate to the `/f:/Work/VerseChat` directory.
4. Run the Flask application:

```sh
python app.py
```

5. Open a web browser and go to `http://127.0.0.1:5000` to access the application.

## Enabling Logging

To enable logging, add the following lines to your `app.py` file:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will enable debug-level logging for your application.

## API Endpoint

You can fetch Bible verses using the following API endpoint:

```
GET /api/get_verse?book=<book>&chapter=<chapter>&verse=<verse>
```

### Example

```sh
curl "http://127.0.0.1:5000/api/get_verse?book=John&chapter=3&verse=16"
```

## Chatbot Feature

You can chat with the Gemini chatbot to fetch Bible verses.

### Example

1. Open the web application in your browser.
2. Type a message like "Get verse John 3:16" in the chat box.
3. The chatbot will respond with the requested Bible verse.

## Features

- Fetch Bible verses by specifying the book, chapter, and verse.
- Display the fetched verse on a web page with an enhanced UI.
- API endpoint for fetching Bible verses programmatically.
- Chatbot interface to interact with the Gemini API.

## Future Enhancements

- User Authentication: Add user login to track who’s sending the verses.
- Chat Interface: Include a more complex chat interface, where the user can send prayers or questions.
- Verse History: Display a history of all verses that have been fetched.
