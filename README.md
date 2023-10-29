 # STELLA - AI Chatbot Documentation
 
 ## Table of Contents

 - [Introduction](#introduction)
 - [Project Structure](#project-structure)
 - [Installation](#installation)
 - [Usage](#usage)
 - [Configuration](#configuration)
 - [Discord Bot](#discord-bot)
 - [Web Interface](#web-interface)
 - [Wikipedia Search](#wikipedia-search)
 - [Error Handling](#error-handling)
 - [Contributing](#contributing)
 - [License](#license)

 ## Introduction
 
STELLA is an AI Chatbot that provides various functionalities through a Discord bot and a web interface. It can answer questions, perform calculations, and search Wikipedia for information. This documentation provides an overview of the project, its structure, installation instructions, and usage guidelines.

 ## Project Structure

 - `chatbot/`: Contains the Python code for the AI chatbot.
 - `assets/`: Stores essential data files and assets.
 - `discord/`: Holds the Discord bot code and configuration.
 - `web/`: Contains the web interface code and assets.
 - `log/`: Contains log files for error and application logs.

 ## Installation
 
1. Clone the repository:

```
git clone https://github.com/BYT-Bender/AI-Chatbot.git
```

2. Set up the Python environment:

```
cd chatbot
pip install -r requirements.txt
```

3. Set up the Discord Bot and Web Interface as described in the respective sections below.

 ## Usage
 
 ### Discord Bot
 
1. Start the Discord bot:

```
python bot.py
```

2. Use the bot on your Discord server by sending messages in the configured channel.

 ### Web Interface
 
1. Start the web interface:

```
cd web
python app.py
```

Access the web interface by opening a web browser and visiting `http://localhost:5000`.

 ### Wikipedia Search
 
STELLA can search Wikipedia for information. To use this feature, simply type `what is <query>` in the Discord channel where the bot is active.

## Error Handling

Error messages are logged in the following files:

 - `log/error.log`: Logs unhandled errors.
 - `log/log_app.txt`: Logs application-related information.
 - `log/log_CL.txt`: Logs command-line interface interactions.
 - `log/log_discord.txt`: Logs Discord bot interactions.
 - `log/log_web.txt`: Logs web interface interactions.

 ## Configuration
 
Customization of STELLA can be done through configuration files and environment variables. Configuration files are stored in the `config/` directory, and environment variables can be set as needed.

 ## Contributing

If you want to contribute to the STELLA project, please follow these steps:

1. Fork the project.
2. Create a new branch.
3. Make your changes.
4. Submit a pull request.

 ## License
This project is licensed under the XYZ License. See the [LICENSE]() file for details.
