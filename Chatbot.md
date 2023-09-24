# Chatbot Documentation

## Table of Contents

- [Overview](#project-overview)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Chatbot Class](#chatbot-class)
- [Methods](#methods)
- [Project Goals](#project-goals)
- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)
- [Project Team](#project-team)
- [Resources](#resources)

## Project Overview

- **Project Title:** AI Chatbot
- **Project Description:** The AI Chatbot using Natural Language Processing (NLP) is an innovative project that aims to create a conversational agent capable of understanding and responding to user input in a natural and engaging way. This AI chatbot leverages the power of NLP techniques to provide human-like interactions and assist users with their queries.
- **Start Date:** Thursday, September 21, 2023 `21/09/2023`
- **End Date:** <span style="color:yellow">Under Development</span>
- **Project Status:** <span style="color:yellow">Under Development</span>

## Installation

To run the Chatbot, follow these steps:

1. Clone the repository or download the source code.
2. Install the required Python libraries listed in the `requirements.txt` file using the command `pip install -r requirements.txt`.
3. (Optional) Edit the `config.json` file (see [Configuration](#configuration)).
4. Run the `chatbot.py` script.

## Configuration

The Chatbot's behavior can be configured using the `config.json` file. Here are the available configuration options:

- `response_file`: Path to the file containing chatbot responses.
- `commands_file`: Path to the file containing admin commands.
- `unrecognized_file`: Path to the file to store unrecognized user messages.
- `system_sound`: Enable system sound alerts (true/false).
- `speak_response`: Enable text-to-speech for bot responses (true/false).
- `voice`: Index of the voice to be used for text-to-speech (0 for male, 1 for female).
- `user_name`: The name to display for the user.
- `bot_name`: The name to display for the chatbot.

Example `config.json`:

```json
{
    "response_file": "responses.csv",
    "commands_file": "admin_commands.csv",
    "unrecognized_file": "unrecognized_messages.csv",
    "system_sound": true,
    "speak_response": true,
    "voice": 1,
    "user_name": "You",
    "bot_name": "Chatbot"
}
```

## Usage

To use the Chatbot, follow these instructions:

1. Run the program by executing `chatbot.py`.
2. Enter your messages in the format: `User: [Your message]`.
3. Type `exit` or `quit` to end the conversation.
4. The Chatbot can also handle admin commands and reloading of responses (see [Methods](#methods)).

## Chatbot Class

The `Chatbot` class represents the core functionality of the chatbot. It is responsible for handling user interactions and managing responses.

## Methods

### `__init__(self, config)`

Initialize the Chatbot with the provided configuration.

- `config` (dict): Configuration settings for the chatbot.

### `reload_responses(self)`

Reload responses from the response file.

### `load_admin_commands(self)`

Load admin commands from the commands file.

### `initialize_tts(self)`

Initialize the text-to-speech engine for the chatbot.

### `preprocess_text(self, text)`

Preprocess and clean the user's input text.

### `match_pattern(self, user_message)`

Find a matching pattern in the user's message.

### `update_unrecognized_file(self, user_message)`

Update the unrecognized messages file with user input.

### `handle_admin_command(self, command)`

Handle admin commands, such as clearing responses or unrecognized messages.

### `clear_responses(self)`

Clear all responses.

### `clear_unrecognized(self)`

Clear unrecognized user messages.

### `clear_file(self, file_path, columns, name)`

Clear a specific file by creating an empty one.

### `generate_response(self, user_message)`

Generate a response based on the user's input.

### `speak(self, text)`

Speak the given text using text-to-speech if enabled.

### `main(self)`

Start the main chat loop for user interaction.

<!-- ## Progress

- [x] #739
- [ ] hello
- [ ] Add delight to the experience when all tasks are complete :tada: -->

## Project Goals

1. **Conversational Understanding:** The primary goal of the project is to enable the chatbot to understand user messages, including text preprocessing, pattern matching, and intent recognition.

2. **Intelligent Responses:** The chatbot will be designed to generate intelligent responses based on recognized user intents, providing relevant and context-aware answers.

3. **User Interaction:** Implement a user-friendly interface that allows users to interact with the chatbot through text input and receive text or speech responses.

4. **Admin Functionality:** Include administrative features to manage and reload chatbot responses, clear unrecognized messages, and handle administrative commands securely.

5. **Text-to-Speech:** Incorporate text-to-speech (TTS) functionality to enable the chatbot to speak its responses, enhancing the user experience.

## Key Features

- **Pattern Matching:** The chatbot employs regular expressions and pattern matching techniques to identify user intents and queries.

- **Response Management:** Responses are managed in a structured manner, allowing for easy updates and customization.

- **User-Friendly Interface:** Users can interact with the chatbot by typing messages, and the chatbot responds with either text or speech.

- **Administrative Commands:** The chatbot recognizes administrative commands and provides secure access to certain functions.

## Technologies Used

- Python for coding the chatbot logic.
- Libraries such as Pandas for data management and Pyttsx3 for text-to-speech.
- Natural Language Processing (NLP) techniques for text preprocessing and intent recognition.

## Future Enhancements

- Expansion of the chatbot's knowledge base and support for a wider range of intents.
- Integration with external APIs for real-time information retrieval.

## Project Team

- Sourabh Srivastva `22760`
- Ashvani `00000`
- Rachit `00000`

## Resources

- [Python](https://www.python.org/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/en/latest/)
- [re Documentation](https://docs.python.org/3/library/re.html)
- [datetime Documentation](https://docs.python.org/3/library/datetime.html)
- [winsound Documentation](https://docs.python.org/3/library/winsound.html)
- [getpass Documentation](https://docs.python.org/3/library/getpass.html)
- [json Documentation](https://docs.python.org/3/library/json.html)
- [TextStyle Documentation](TextStyle.md)