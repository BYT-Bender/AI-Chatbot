# Release Note for AI Chatbot

## 1.0.0

### New Features

- Chatbot recognizes user queries through predefined patterns.
- Customizable responses associated with patterns or user messages.
- Consistent text preprocessing for enhanced matching.
- Logging of unrecognized messages.
- Set of secure admin commands.
    - `reload patterns`
    - `reload responses`
    - `reload admin commands`
- Vocalization of responses using pyttsx3 library.
- User-friendly exit with "exit" or "quit."
- Validation of admin commands and passwords.


## 1.1.0

### New Features

- Integrate Flask server with a web interface.
- Introduced Python GUI application.

## 1.1.1

### Enhancements

- Added light, dark, and system appearance modes for the Python application.
- Enabled adjustable UI scaling for a more personalized user experience.


## 1.2.0

### New Features

- Settings customization through config.json.
- Dynamic asset initialization.
- Enhanced sound notifications with varied frequencies.

### Enhancements

- Improved handling of leading/trailing whitespaces.
- Patterns and intents consolidated in intents_data.py.


## 1.3.0

### Major Changes

- Comprehensive error handling during critical processes.
- Configurable chatbot voice through `config.json`.
- Checks for required modules during startup.
- New formatting.py for customizable text styles.

### Improvements and Fixes

- Graceful handling of FileNotFoundError.
- Color-coded feedback messages on reload status.
- Improved handling for invalid commands and password mismatches.
- More robust TTS engine initialization.
- Clear error message and graceful exit for missing config file.


## 2.0.0

### New Features

- Flask integration for web-based UI.
- Integrated TTS for spoken responses.
- Response usage analysis with `analize.py`.

### Enhancements

- Dynamic response reloading during runtime.
- Improved error logging for troubleshooting.
- Responses and commands loaded from external files.
- Documentation and Additional Files.
- Included requirements.txt for easy dependency installation.

### Bug Fixes

- Improved handling of special characters and whitespace.
- Enhanced exception handling for better error reporting.


## 3.0.0 (Stable)

### New Features

- Chatbot provides details about chemical elements.
- Sleek GUI using tkinter for user-friendly interaction.
- Track command and response usage for analysis.
- Module for matching user messages to predefined patterns.
- Searches for response on wikipedia.

### Code Organization

- Code organized into separate files for modularity.
- Improved readability with files like chatbot.py and gui.py.
- Comprehensive element data in the elements folder.
- Utility module for logging and error handling.

### Bug Fixes

- Changed admin_commands.csv to admin_commands.json.
- Improved data handling and error logging.

### Enhancements

- System sound alert upon startup.
- Configuration for chatbot voice.
- Improved fallback response for user engagement.

### Known Issues

- Minor GUI layout issues on different screen sizes.
- Ensure accuracy of chemical element data.


Version 7.0 (Stable)
Features and Enhancements
Major Code Refactoring (7.0.1)
Significant restructuring and cleanup for better maintainability.
GUI Integration (7.0.2)
Introduction of a graphical user interface for user-friendly interaction.
Server Integration (7.0.3)
Accessibility through a Flask server for web-based interactions.
Voice Interaction (7.0.4)
Text-to-Speech (TTS) functionality for spoken responses.
Element Searching (7.0.5)
Feature to search for elements based on user queries.
Wikipedia Search (7.0.6)
Improved Wikipedia search for accurate and informative responses.
Command Usage Tracking (7.0.7)
Enhanced tracking of command usage for better analysis.
Admin Commands (7.0.8)
Additional admin commands for control and management.
Error Handling (7.0.9)
Improved error handling and logging mechanisms.
Documentation Updates (7.0.10)
Updated documentation to reflect changes.
Bug Fixes
Unrecognized Message Tracking (7.0.11)
Fixed issues related to tracking unrecognized messages.
Configuration Loading (7.0.12)
Improved configuration loading for graceful handling.
Other Changes
File and Directory Verification (7.0.13)
Script to check presence of expected files and directories.
File Structure Information (7.0.14)
Document detailing the file structure for better understanding.

------

## Version 1.0

### Features:

1. **Pattern Matching:** The chatbot uses a set of predefined patterns to recognize user queries. These patterns are defined in the `patterns.csv` file, and when a user's message matches one of these patterns, the bot provides a predefined response.

2. **Response Management:** The chatbot's responses are stored in the `responses.csv` file. Responses can be customized and associated with specific patterns or user messages, allowing for tailored interactions.

3. **Unrecognized Message Tracking:** When a user's message does not match any predefined pattern or response, the chatbot logs these unrecognized messages into the `unrecognized.csv` file, along with a timestamp and a count of occurrences.

4. **Text Preprocessing:** User messages are preprocessed to ensure consistency. The chatbot converts all text to lowercase and removes punctuation to enhance pattern matching and response retrieval.

5. **Admin Commands:** The chatbot offers a set of admin commands for managing patterns, responses, and unrecognized messages. Admin commands are secured with a password and a prefix, and they can be customized. Admin commands include:

    - Clearing Patterns
    - Clearing Responses
    - Clearing Unrecognized Messages

6. **Reloading Data:** The chatbot allows for reloading data files during runtime. Users can issue a "reload" command to reload patterns, responses, or admin commands individually or all together.

7. **Text-to-Speech (TTS):** The chatbot utilizes the `pyttsx3` library for text-to-speech functionality. It can vocalize responses to provide a more interactive experience.

8. **Exit Command:** Users can end the conversation with the chatbot at any time by typing "exit" or "quit."

9. **Customizable Admin Password and Prefix:** The admin password and prefix can be customized by modifying the `admin_commands.csv` file.

10. **Default Data Files:** The chatbot comes with default data files for patterns, responses, and admin commands. These files are loaded during initialization but can be modified to suit specific needs.

11. **Voice Selection:** The chatbot can select different voices for TTS, allowing for a more personalized interaction.

12. **Feedback for Reloading:** When data files are reloaded, the chatbot provides feedback on the successful reloading of patterns, responses, and admin commands.

13. **Protection against Invalid Commands:** The chatbot validates admin commands and passwords to protect against unauthorized access.

14. **Clearing Data:** Admin commands allow for clearing patterns, responses, or unrecognized messages, maintaining data hygiene.

15. **End User Instructions:** The chatbot provides clear instructions to the user, indicating how to end the conversation and prompting admin commands.

16. **Input Validation:** The chatbot is designed to handle user input gracefully, including reloading and admin commands.

17. **Rephrasing Prompt:** When a user query does not match any defined pattern, the chatbot politely requests the user to rephrase the question.

This initial version of the chatbot provides a foundation for interactive conversations, with a focus on pattern matching and response management, while also offering administrative features for maintaining data integrity and customization.






## Version 2.0

### New Features:

1. **Integration with Flask Web Server:**

    - The chatbot is now integrated with a Flask web server, enabling users to interact with the chatbot via a web interface.

2. **Web Interface:**

    - The chatbot includes a web interface provided by the index.html file. Users can access the chatbot by opening a web browser and navigating to the web interface.

3. **RESTful API for Chatbot Interaction:**

The Flask web server exposes a RESTful API endpoint at /process. Users can send POST requests with user input to this endpoint, and the chatbot will respond with JSON-formatted replies.
Serving Static Assets:

The Flask web server serves static assets (e.g., images and CSS files) located in the assets folder, including a picture of Stella and a style.css file for styling the web interface.
Sound Notifications:

The chatbot provides sound notifications using the winsound library to alert users when it is reloaded successfully.
Improved Pattern Matching:

The chatbot uses a more sophisticated pattern matching approach by searching for patterns within the user's message. It also utilizes a preprocessing step to remove unnecessary white spaces and non-alphanumeric characters for enhanced pattern matching accuracy.
Intent-Based Responses:

The chatbot has been updated to use intents for generating responses. Intents are defined in the intents_data.py file, and user messages are matched to these intents, allowing for more dynamic and context-aware responses.
Data Files Organization:

The data files, including responses, admin commands, and unrecognized messages, are organized in the data folder for improved file management and organization.
Enhancements:

Customizable Admin Commands:

Admin commands are now defined in the admin_commands.csv file, allowing for customization of admin commands and the admin prefix.
Clearing Responses and Unrecognized Messages:

Admin commands have been updated to provide the ability to clear responses and unrecognized messages while maintaining data integrity.
Text-to-Speech (TTS):

The chatbot continues to use the pyttsx3 library for text-to-speech functionality to provide interactive responses.
User-Friendly Exit:

The chatbot allows users to exit the conversation by typing "exit" or "quit."
How to Use:

To interact with the chatbot via the web interface, simply run the server.py file, and access the chatbot in a web browser.
You can also use the chatbot in the console as demonstrated in the root.py file.
Additional Files:

The intents_data.py file contains the intent data used by the chatbot for pattern matching and response generation.
The index.html file provides the web interface for the chatbot, and it should be accessible in the root directory of the Flask web server.
This updated version of the chatbot provides a web interface, RESTful API for easy interaction, improved pattern matching, and support for intent-based responses, enhancing the user's experience and providing more dynamic and context-aware conversations.
