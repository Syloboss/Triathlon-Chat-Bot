import json
import random
import datetime
from difflib import get_close_matches
import tkinter as tk
from tkinter import scrolledtext, simpledialog
import pytz
import textwrap
from PIL import Image, ImageTk
from tkinter import ttk

# Configuration
KB_FILE_PATH = "/Users/yannickhefti/Yannick Hefti/UNI/HSG/4. Sem/CS/Group Project/knowledge_base.json"
LOGO_PATH = "/Users/yannickhefti/Yannick Hefti/UNI/HSG/4. Sem/CS/Group Project/triathlon_chatbot_logo.png"
WINDOW_SIZE = "600x700"
WINDOW_TITLE = "Chatbot"
BACKGROUND_COLOR = "#d3d0d0"

# Load data from a JSON file.
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save data to a JSON file with indentation.
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Find the closest match to a user's question from a list of questions.
def find_best_match(user_question, questions):
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.8) #80% match with question
    return matches[0] if matches else None

# Retrieve the answer for a given question from the knowledge base.
def get_answer(question, knowledge_base):
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

# Create the main user interface.
def create_ui():
    knowledge_base = load_json(KB_FILE_PATH)
    window = create_window(WINDOW_SIZE, WINDOW_TITLE, BACKGROUND_COLOR)
    logo_image = load_and_resize_image(LOGO_PATH, (70, 70))
    setup_ui_elements(window, logo_image, knowledge_base)
    window.mainloop()

# Initialize the main window with given properties.
def create_window(size, title, bg_color):
    window = tk.Tk()
    window.title(title)
    window.geometry(size)
    window.configure(bg=bg_color)
    return window

# Load and resize an image from the given path.
def load_and_resize_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize(size)
    return ImageTk.PhotoImage(image)

# Setup UI components within the window.
def setup_ui_elements(window, logo_image, knowledge_base):
    logo_label = tk.Label(window, image=logo_image, borderwidth=0, bg=BACKGROUND_COLOR)
    logo_label.pack(pady=0)

    chat_history = scrolledtext.ScrolledText(window, width=70, height=30, font=("Arial", 14), bg="light yellow", fg="black", borderwidth=0, highlightthickness=0)
    chat_history.pack(pady=0)

    # Insert a random initial phrase into the chat history
    initial_phrases = ["Hello! How can I help you today?", 
                       "Hi there! What can I do for you?",
                       "What's on your mind?", "How can I assist you today?", 
                       "I'm here to assist you. What do you need?", 
                       "What can I help you with today?"]
    chat_history.insert(tk.END, "Bot: " + random.choice(initial_phrases) + "\n")

    user_input = tk.Entry(window, width=60, font=("Arial", 14), bg="light cyan", fg="black", borderwidth=0, highlightthickness=0)
    user_input.insert(0, "Enter message")
    user_input.pack(pady=10)

    bind_user_input_events(user_input, chat_history, knowledge_base)
    setup_control_buttons(window, chat_history, user_input, knowledge_base)  # Pass user_input and knowledge_base

# Bind events to user input for interaction.
def bind_user_input_events(user_input, chat_history, knowledge_base):
    user_input.bind('<FocusIn>', lambda event: user_input.delete(0, "end"))
    user_input.bind('<Return>', lambda event: process_user_message(user_input.get(), chat_history, knowledge_base, user_input))

# Setup control buttons for user interactions.
def setup_control_buttons(window, chat_history, user_input, knowledge_base):
    style = ttk.Style(window)
    style.theme_use('alt')  

    button_frame = tk.Frame(window, bg=BACKGROUND_COLOR)
    button_frame.pack(pady=10)

    clear_button = ttk.Button(button_frame, text="Clear Chat", command=lambda: chat_history.delete(1.0, tk.END), style='my.TButton')
    clear_button.pack(side=tk.LEFT, padx=40)
    send_button = ttk.Button(button_frame, text="Send", command=lambda: process_user_message(user_input.get(), chat_history, knowledge_base, user_input), style='my.TButton')
    send_button.pack(side=tk.LEFT, padx=40)
    quit_button = ttk.Button(button_frame, text="Quit", command=window.destroy, style='my.TButton')
    quit_button.pack(side=tk.LEFT, padx=40)

    style.configure('my.TButton', relief='flat', borderwidth=0)


# Process user message, interact with chat history and knowledge base.
def process_user_message(message, chat_history, knowledge_base, user_input):
    chat_history.insert(tk.END, f"You: {message}\n")
    user_input.delete(0, tk.END)
    handle_message_logic(message, chat_history, knowledge_base)

# Logic to handle different types of messages.
def handle_message_logic(message, chat_history, knowledge_base):
    message_lower = message.lower()  # Convert message to lower case for case-insensitive matching
    if 'quote' in message_lower and 'motivational' in message_lower:
        display_motivational_quote(chat_history, knowledge_base['motivational_quotes'])
    elif message_lower in ['quit', 'exit', 'bye']:
        chat_history.master.destroy()
    else:
        # Look for keywords or specific questions in the message
        response = check_keywords(message, knowledge_base['keywords'], knowledge_base['responses'])
        if response:
            chat_history.insert(tk.END, f"Bot: {response}\n")
        else:
            # Try finding a close match to user questions within the knowledge base
            questions = [q['question'] for q in knowledge_base['questions']]
            best_match = find_best_match(message, questions)
            if best_match:
                answer = get_answer(best_match, knowledge_base)
                chat_history.insert(tk.END, f"Bot: {answer}\n")
            else:
                chat_history.insert(tk.END, "Bot: I don't know the answer. Can you teach me?\n")
                new_answer = simpledialog.askstring("New Answer", "Type the answer or cancel to skip:")
                if new_answer:
                    knowledge_base['questions'].append({'question': message, 'answer': new_answer})
                    save_json(KB_FILE_PATH, knowledge_base)
                    chat_history.insert(tk.END, "Bot: Thank you! I've learned a new response.\n")
                else:
                    chat_history.insert(tk.END, "Bot: No problem! Ask me something else or teach me another time.\n")

# Check if the user message contains any of the defined keywords and return the corresponding response.
def check_keywords(message, keywords, responses):
    message_lower = message.lower()  # Convert message to lower case for case-insensitive matching
    for keyword, keys in keywords.items():
        if all(key.lower() in message_lower for key in keys):
            return responses[keyword]
    return None

# Display a random motivational quote in the chat history.
def display_motivational_quote(chat_history, quotes):
    quote = random.choice(quotes)
    wrapped_quote = textwrap.fill(quote, width=85)
    chat_history.insert(tk.END, f"Bot: {wrapped_quote}\n")

if __name__ == '__main__':
    create_ui()
