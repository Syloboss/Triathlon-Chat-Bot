
# Chatbot for Triathlon Enthusiasts

## Overview
This Python-based chatbot application provides a friendly user interface for triathlon enthusiasts to interact with. Using the Tkinter library, it supports answering queries related to triathlon based on a predefined knowledge base. The application is capable of handling specific questions, providing motivational quotes, and learning from user inputs.

## Features
- User-friendly graphical interface built with Tkinter.
- Loads questions and answers from a JSON-formatted knowledge base.
- Supports dynamic interactions where the bot learns from user inputs.
- Displays a chat history with options to clear chat or quit the application.
- Logo and chat interface.

## Prerequisites
Before you can run this chatbot, you'll need the following installed on your system:
- Python 3.8 or higher
- Tkinter library
- PIL (Pillow) for image handling
- PyTZ for timezone adjustments

## Installation
1. Ensure Python and necessary libraries are installed:
   ```
   pip install tkinter Pillow pytz
   ```
2. Clone the repository or download the source code.

## Usage
To run the chatbot, execute the following command in the terminal:
```
python path_to_chatbot_script.py
```
Make sure to replace `path_to_chatbot_script.py` with the actual path to the Python script.

## Configuration
- `KB_FILE_PATH`: Path to the knowledge base JSON file.
- `LOGO_PATH`: Path to the logo image.
- `WINDOW_SIZE`, `WINDOW_TITLE`, `BACKGROUND_COLOR`: Configuration for the GUI window appearance.

