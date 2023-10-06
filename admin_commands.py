import json
from getpass import getpass
import winsound

import pandas as pd

from formatting import TextStyle
from utilities import Utility

class AdminCommands:
    def __init__(self, config):
        self.config = config
        self.admin_prefix = self.config["admin_prefix"]
        self.log_action = Utility(self.config).log_action
        self.load_admin_commands()
        self.load_responses()

    def load_admin_commands(self):
        try:
            commands_df = pd.read_csv(self.config["commands_file"], encoding="utf-8")

            self.admin_commands = {}
            for index, row in commands_df.iterrows():
                command = row["command"]
                function = row["function"]
                arguments = row["arguments"]
                password = row["password"]
                if not pd.isna(arguments):
                    arguments = [arg.strip() for arg in arguments.split(",") if arg.strip()]
                else:
                    arguments = []
                self.admin_commands[command] = {"function": function, "arguments": arguments, "password": password}

            self.log_action(f'Successfully loaded Commands file ({self.config["commands_file"]})')
        except FileNotFoundError:
            print(f"{TextStyle.fg['R']}Error: Commands file not found.{TextStyle.fg['x']}")
            self.log_action(f'FileNotFoundError: Commands file ({self.config["commands_file"]})')
            raise
        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred while loading admin commands: {error}{TextStyle.fg['x']}")
            self.log_action(f'Failed to load Commands file ({self.config["commands_file"]})')
            raise

    def handle_admin_command(self, command):
        try:
            if command not in self.admin_commands:
                print(f"{TextStyle.fg['Y']}Invalid command.{TextStyle.fg['x']}")
                self.log_action(f'Invalid command: {command}')
                return

            command_info = self.admin_commands[command]
            function_name = command_info["function"]
            arguments = command_info["arguments"]
            password = command_info.get("password", None)

            if not hasattr(self, function_name) or not callable(getattr(self, function_name)):
                print(f"{TextStyle.fg['Y']}Invalid command: Function not found.{TextStyle.fg['x']}")
                self.log_action(f"Invalid command: Can't find instance of `{function_name}`")
                return

            if not pd.isna(password):
                password_in = getpass(f"{TextStyle.fg['B']}Enter admin password: {TextStyle.fg['x']}")
                if password_in != password:
                    print(f"{TextStyle.fg['Y']}Invalid password.{TextStyle.fg['x']}")
                    self.log_action(f'Invalid password.')
                    return

            function_to_execute = getattr(self, function_name)
            function_to_execute(*arguments)

        except Exception as error:
            print(f"{TextStyle.fg['R']}Error handling admin command: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error handling admin command: {error}')

    def clear_responses(self):
        try:
            self.clear_file(self.config["response_file"], ["response_id", "bot_response"], "Responses")
        except:
            raise

    def clear_unrecognized(self):
        try:
            self.clear_file(self.config["unrecognized_file"], ["count", "time", "user_message"], "Unrecognized chat")
        except:
            raise

    def clear_file(self, file_path, columns, name):
        try:
            pd.DataFrame(columns=columns).to_csv(file_path, mode="w", header=True, index=False)
            print(f"{TextStyle.fg['G']}{name} cleared...{TextStyle.fg['x']}")
            self.log_action(f'Cleared {name}')
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error clearing {name.lower()}: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error clearing: {name.lower()}')

    def reload_chatbot(self, reload_responses=False, reload_admin_commands=False):
        try:
            if reload_responses:
                self.load_responses()
                print(f"{TextStyle.fg['G']}Responses reloaded successfully...{TextStyle.fg['x']}")

            if reload_admin_commands:
                self.load_admin_commands()
                print(f"{TextStyle.fg['G']}Admin Commands reloaded successfully...{TextStyle.fg['x']}")

            if self.config["system_sound"]:
                winsound.Beep(1000, 500)

        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during Chatbot reload: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error during Chatbot reload: {error}')

    def load_responses(self):
        try:
            with open(self.config["response_file"], "r") as intents_file:
                intents_data = json.load(intents_file)
                self.intents = intents_data.get("intents", [])
            self.log_action(f'Successfully loaded Response file ({self.config["response_file"]})')
        except FileNotFoundError:
            print(f"{TextStyle.fg['R']}Error: Response file not found.{TextStyle.fg['x']}")
            self.log_action(f'FileNotFoundError: Response file ({self.config["response_file"]})')
            raise
        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred while loading responses: {error}{TextStyle.fg['x']}")
            self.log_action(f'Failed to load Response file ({self.config["response_file"]})')
            raise