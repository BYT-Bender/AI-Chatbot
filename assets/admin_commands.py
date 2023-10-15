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
        self.utility = Utility(self.config)
        self.load_admin_commands(show=False)
        self.load_responses(show=False)
        self.exit = self.utility.exit

    def load_admin_commands(self, show=True):
        try:
            with open(self.config["admin_command_file"], 'r', encoding='utf-8') as json_file:
                commands_data = json.load(json_file)

            self.admin_commands = {cmd['command']: cmd for cmd in commands_data}
            self.utility.handle_success("Loaded", "Admin Command", self.config["admin_command_file"], show)
        except FileNotFoundError:
            self.utility.handle_file_not_found_error("Admin Command", self.config["admin_command_file"])
        except Exception as error:
            self.utility.handle_error("Loading Admin Commands", error)

    def handle_admin_command(self, command):
        try:
            command_info = self.admin_commands.get(command)

            if not command_info:
                self.utility.handle_invalid_command(command)
                return

            command_id = command_info["id"]
            function_name = command_info["function"]
            arguments = command_info["arguments"]
            password = command_info.get("password")

            if not hasattr(self, function_name) or not callable(getattr(self, function_name)):
                self.utility.handle_invalid_function(command, function_name)
                return

            if password and not self.verify_password(password):
                self.utility.handle_invalid_password()
                return

            self.utility.update_usage(self.config["command_usage"], command_id, "updating command usage data")
            self.utility.handle_command_use(command, function_name, arguments)
            function_to_execute = getattr(self, function_name)
            function_to_execute(*arguments)

        except Exception as error:
            self.utility.handle_error("handling admin commands", error)

    def clear_responses(self):
        self.clear_file(self.config["response_file"], ["response_id", "bot_response"], "Responses")

    def clear_unrecognized(self):
        self.clear_file(self.config["unrecognized_file"], ["count", "time", "user_message"], "Unrecognized chat")

    def clear_file(self, file_path, columns, name):
        try:
            pd.DataFrame(columns=columns).to_csv(file_path, mode="w", header=True, index=False)
            self.utility.handle_success("Cleared", name, file_path)
        except Exception as error:
            self.utility.handle_error(f"clearing {name}", error)

    def reload_chatbot(self, reload_responses=False, reload_admin_commands=False):
        try:
            if reload_responses:
                self.load_responses()

            if reload_admin_commands:
                self.load_admin_commands()

            if self.config["system_sound"]:
                winsound.Beep(1000, 500)

        except Exception as error:
            self.utility.handle_error("Chatbot reload", error)

    def load_responses(self, show=True):
        try:
            with open(self.config["response_file"], "r") as intents_file:
                intents_data = json.load(intents_file)
                self.intents = intents_data.get("intents", [])
            self.utility.handle_success("Loaded", "Response", self.config["response_file"], show)
        except FileNotFoundError:
            self.utility.handle_file_not_found_error("Response", self.config["response_file"])
        except Exception as error:
            self.utility.handle_error("responses", error)

    def verify_password(self, password):
        password_in = getpass(f"{TextStyle.fg['B']}Enter admin password: {TextStyle.fg['x']}")
        return password_in == password

