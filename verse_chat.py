import tkinter as tk
from tkinter import scrolledtext
import requests

# Function to get Bible verse
def get_bible_verse():
    # Get user input
    book = book_entry.get()
    chapter = chapter_entry.get()
    verse = verse_entry.get()

    # URL for Bible API (using Bible-API.com)
    url = f"https://bible-api.com/{book}%20{chapter}:{verse}"

    # Make a GET request to fetch the verse
    response = requests.get(url)
    
    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()
        verse_text = data['verse']
        # Display the verse in the chat
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"Verse: {book} {chapter}:{verse}\n{verse_text}\n\n")
        chat_display.config(state=tk.DISABLED)
    else:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, "Sorry, we couldn't find that verse. Please try again.\n\n")
        chat_display.config(state=tk.DISABLED)

# Set up the main window
root = tk.Tk()
root.title("VerseChat")

# Set up the chat display area (scrollable text box)
chat_display = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
chat_display.grid(row=0, column=0, padx=10, pady=10)
chat_display.config(state=tk.DISABLED)

# Label and entry for book name
book_label = tk.Label(root, text="Book:")
book_label.grid(row=1, column=0, padx=10, pady=5)
book_entry = tk.Entry(root, width=20)
book_entry.grid(row=1, column=1, padx=10, pady=5)

# Label and entry for chapter
chapter_label = tk.Label(root, text="Chapter:")
chapter_label.grid(row=2, column=0, padx=10, pady=5)
chapter_entry = tk.Entry(root, width=20)
chapter_entry.grid(row=2, column=1, padx=10, pady=5)

# Label and entry for verse
verse_label = tk.Label(root, text="Verse:")
verse_label.grid(row=3, column=0, padx=10, pady=5)
verse_entry = tk.Entry(root, width=20)
verse_entry.grid(row=3, column=1, padx=10, pady=5)

# Submit button to fetch the verse
submit_button = tk.Button(root, text="Get Verse", command=get_bible_verse)
submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Run the application
root.mainloop()
