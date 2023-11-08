 # STELLA - Configuration Guide

STELLA is an AI Chatbot that you can configure to perform various tasks. This guide will walk you through the steps to configure the STELLA bot for your specific needs. Make sure you have already installed the bot as described in the [Installation section](README.md) of the main documentation.

 ## Table of Contents

 - [Bot Configuration]()
 - [Discord Configuration]()
 - [Wikipedia Configuration]()

 ## Bot Configuration

 Before diving into specific functionalities, it's essential to understand how to configure the STELLA bot. The main configuration file is `config.json`, located in the root directory. You can adjust the following settings:

 `"parent_directory"`: Set the parent directory path where your bot resides. Update this path to match your project's location.

`"log_files"`: Define the paths for different log files. By default, the bot logs interactions and errors in different files. You can customize these paths to suit your preferences.

`"user_agent"`: Configure the user agent for web requests made by the bot. The default user agent is set to "STELLA Bot 1.0."

`"data"`: Specify the data files and directories used by the bot.

  `"element"`: Configure the data related to chemical elements. You can customize the `"data"` and `"intents"` file paths.

  `"conversation"`: Configure the conversation intents used by the bot. Customize the `"data"` and `"intents"` file paths as needed.

  `"wikipedia"`: Configure the Wikipedia search functionality. You can adjust the `"user_agent"` and define other settings specific to Wikipedia searches.

Here's a sample configuration:

```JSON
{
    "parent_directory": "/path/to/your/project",
    "log_files": {
        "app": "log/log_app.txt",
        "cl": "log/log_CL.txt",
        "discord": "log/log_discord.txt",
        "web": "log/log_web.txt"
    },
    "user_agent": "Your User Agent",
    "data": {
        "element": {
            "data": "assets/responses/elements/elements.json",
            "intents": "assets/responses/elements/search_element.json"
        },
        "conversation": {
            "data": "assets/responses/conversation/conversation.json",
            "intents": "assets/responses/conversation/search_conversation.py"
        },
        "wikipedia": {
            "user_agent": "Your Wikipedia User Agent"
        }
    }
}
```

## Discord Configuration

STELLA operates as a Discord bot, and you can configure it to interact with your Discord server. Ensure that you've created a Discord bot account and obtained the bot token. This token should be stored in the `.env` file in the `discord/` directory.

Open the `.env` file and configure the following variables:

 - `DISCORD_TOKEN`: Replace `<DISCORD_BOT_TOKEN>` with your actual bot token.
 - `DISCORD_GUILD`: Set the guild (server) name to define where the bot can operate.

Example:

```Dotenv
DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN"
DISCORD_GUILD="YOUR_SERVER_NAME"
```

 ## Wikipedia Configuration

STELLA can perform Wikipedia searches. To configure this feature, you need to ensure the bot can access Wikipedia.

1. Open the main configuration file (`config.json`) in the root directory and update the `"user_agent"` under `"wikipedia"` to match a valid user agent for Wikipedia.

Example:

```JSON
"wikipedia": {
    "user_agent": "Your Wikipedia User Agent"
}
```

2. Ensure that your server running the bot has internet access, as the bot requires internet connectivity to fetch information from Wikipedia.

With these configurations in place, the STELLA bot can effectively function in your Discord server and respond to Wikipedia search queries.

This documentation should help you configure the STELLA bot to suit your needs. Customize the bot's behavior and functionalities as required for your specific use case.
