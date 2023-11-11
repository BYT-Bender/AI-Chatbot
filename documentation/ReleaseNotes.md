# Release Notes for AI Chatbot

## 1.0.0 (Alpha)

> July 13, 2023

### New Features

- Chatbot recognizes user queries through predefined patterns.
- Customizable responses associated with patterns or user messages.
- Consistent text preprocessing for enhanced matching.
- Logging of unrecognized messages.
- Set of secure admin commands:
  - `reload patterns`
  - `reload responses`
  - `reload admin commands`
- Vocalization of responses using the pyttsx3 library.
- User-friendly exit with "exit" or "quit."
- Validation of admin commands and passwords.

## 1.1.0

> July 21, 2023

### New Features

- Integrated Flask server with a web interface.
- Introduced Python GUI application.

## 1.1.1

> July 22, 2023

### Enhancements

- Added light, dark, and system appearance modes for the Python application.
- Enabled adjustable UI scaling for a more personalized user experience.

## 1.2.0

> September 24, 2023

### New Features

- Settings customization through `config.json`.
- Dynamic asset initialization.
- Enhanced sound notifications with varied frequencies.

### Enhancements

- Improved handling of leading/trailing whitespaces.
- Patterns and intents consolidated in `intents_data.py`.

## 1.3.0

> September 26, 2023

### Major Changes

- Comprehensive error handling during critical processes.
- Configurable chatbot voice through `config.json`.
- Checks for required modules during startup.
- New `formatting.py` for customizable text styles.

### Improvements and Fixes

- Graceful handling of `FileNotFoundError`.
- Color-coded feedback messages on reload status.
- Improved handling for invalid commands and password mismatches.
- More robust TTS engine initialization.
- Clear error message and graceful exit for missing config file.

## 2.0.0 (Beta)

> October 2, 2023

### New Features

- Flask integration for web-based UI.
- Integrated TTS for spoken responses.
- Response usage analysis with `analize.py`.

### Enhancements

- Dynamic response reloading during runtime.
- Improved error logging for troubleshooting.
- Responses and commands loaded from external files.
- Documentation and Additional Files.
- Included `requirements.txt` for easy dependency installation.

### Bug Fixes

- Improved handling of special characters and whitespace.
- Enhanced exception handling for better error reporting.

## 3.0.0 (RC)

> October 14, 2023

### New Features

- Chatbot provides details about chemical elements.
- Sleek GUI using tkinter for user-friendly interaction.
- Track command and response usage for analysis.
- Module for matching user messages to predefined patterns.
- Searches for response on Wikipedia.
- Utility module for logging and error handling.

### Code Organization

- Code organized into separate files for modularity.
- Improved readability with files like `chatbot.py` and `gui.py`.
- Comprehensive element data in the `elements` folder.

### Bug Fixes

- Changed `admin_commands.csv` to `admin_commands.json`.
- Improved data handling and error logging.

### Enhancements

- System sound alert upon startup.
- Configuration for chatbot voice.
- Improved fallback response for user engagement.

### Known Issues

- Minor GUI layout issues on different screen sizes.
- Ensure accuracy of chemical element data.

## 4.0.0 (Stable)

> November 8, 2023

### Features

- Significant restructuring and cleanup for better maintainability.
- Introduction of a graphical user interface for user-friendly interaction.
- Accessibility through a Flask server for web-based interactions.
- Feature to search for elements based on user queries.

### Enhancements

- Improved Wikipedia search for accurate and informative responses.
- Enhanced tracking of command usage for better analysis.
- Additional admin commands for control and management.
- Improved error handling and logging mechanisms.
- Updated documentation to reflect changes.

### Bug Fixes

- Fixed issues related to tracking unrecognized messages.
- Improved configuration loading for graceful handling.

### Other Changes

- Script to check the presence of expected files and directories.
- Document detailing the file structure for better understanding.
