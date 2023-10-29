# Copyright © 2023 BYT-Bender

# Import necessary modules
import json
from getpass import getpass
import winsound
import pandas as pd

# Import classes and functions from custom modules
from formatting import TextStyle
from utilities import Utility
from analize import Graph


# Define the AdminCommands class
class AdminCommands:
    def __init__(self, config):
        self.config = config
        self.admin_prefix = self.config["admin_prefix"]
        self.utility = Utility(self.config)
        self.graph = Graph(self.config)
        self.load_admin_commands(show=False)
        self.load_conversation_responses(show=False)
        self.load_element_responses(show=False)
        self.exit = self.utility.exit
        self.analize = self.graph.main

    # Load admin commands from a JSON file
    def load_admin_commands(self, show=True):
        try:
            with open(self.config["data"]["command"]["data"], "r", encoding="utf-8") as json_file:
                commands_data = json.load(json_file)

            self.admin_commands = {cmd["command"]: cmd for cmd in commands_data}
            self.utility.handle_success("Loaded", "Admin Command", self.config["data"]["command"]["data"], show)
        except FileNotFoundError:
            self.utility.handle_file_not_found_error("Admin Command", self.config["data"]["command"]["data"])
        except Exception as error:
            self.utility.handle_error("Loading Admin Commands", error)

    # Load responses from a JSON file
    def load_conversation_responses(self, show=True):
        try:
            with open(self.config["data"]["conversation"]["data"], "r") as intents_file:
                intents_data = json.load(intents_file)
                self.conversation_intents = intents_data.get("intents", [])
            self.utility.handle_success("Loaded", "Conversation Response", self.config["data"]["conversation"]["data"], show)
        except FileNotFoundError:
            self.utility.handle_file_not_found_error("Conversation Response", self.config["data"]["conversation"]["data"])
        except Exception as error:
            self.utility.handle_error("Loading Conversation Responses", error)

    # Load element responses from a JSON file                      # NEED WORK (different intents structure)
    def load_element_responses(self, show=True):
        try:
            with open(self.config["data"]["element"]["data"], "r") as intents_file:
                intents_data = json.load(intents_file)
                self.element_intents = intents_data.get("intents", [])
            self.utility.handle_success("Loaded", "Element Response", self.config["data"]["element"]["data"], show)
        except FileNotFoundError:
            self.utility.handle_file_not_found_error("Element Response", self.config["data"]["element"]["data"])
        except Exception as error:
            self.utility.handle_error("Loading Element Responses", error)

    # Handle admin commands based on user input
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

            self.utility.update_usage(self.config["data"]["command"]["usage"], command_id, "updating command usage data")
            self.utility.handle_command_use(command, function_name, arguments)
            function_to_execute = getattr(self, function_name)
            function_to_execute(**arguments)

        except Exception as error:
            self.utility.handle_error("handling admin commands", error)

    # Clear command usage data
    def clear_command_usage(self):
        self.clear_file(self.config["data"]["command"]["usage"], ["id", "count"], "Command usage")

    # Clear conversation response usage data
    def clear_conversation_response_usage(self):
        self.clear_file(self.config["data"]["conversation"]["usage"], ["id", "count"], "Conversation response usage")

    # Clear response usage data
    def clear_response_usage(self):
        self.clear_file(self.config["data"]["common"]["response_usage"], ["date", "response_type", "count"], "Response usage")

    # Clear unrecognized chat data
    def clear_unrecognized(self):
        self.clear_file(self.config["data"]["common"]["unrecognized_file"], ["count", "time", "user_message"], "Unrecognized chat")

    def clear_file(self, file_path, columns, name):
        try:
            pd.DataFrame(columns=columns).to_csv(file_path, mode="w", header=True, index=False)
            self.utility.handle_success("Cleared", name, file_path)
        except Exception as error:
            self.utility.handle_error(f"clearing {name}", error)

    # Reload the chatbot with updated data
    def reload_chatbot(self, reload_conversation_responses=False, reload_admin_commands=False, reload_element_responses=False, all=False):
        try:
            if all or reload_conversation_responses:
                self.load_conversation_responses()

            if all or reload_admin_commands:
                self.load_admin_commands()

            if all or reload_element_responses:
                self.load_element_responses()

            if self.config["system_sound"]:
                winsound.Beep(1000, 500)

        except Exception as error:
            self.utility.handle_error("Chatbot reload", error)

    # Verify an admin password input
    def verify_password(self, password):
        password_in = getpass(f"{TextStyle.fg['B']}Enter admin password: {TextStyle.fg['x']}")
        return password_in == password
