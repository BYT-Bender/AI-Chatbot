# Copyright © 2023 BYT-Bender

import json
import random
from datetime import datetime
import winsound

import pyttsx3
import pandas as pd
import re

from admin_commands import AdminCommands
from formatting import TextStyle
from utilities import Utility
from wikipedia_search import WikipediaSearch

class Chatbot:
    # Initializing assest
    def __init__(self, config):
        self.config = config
        
        self.utility = Utility(self.config)
        self.wikipedia_search = WikipediaSearch(self.config)
        self.admin_commands = AdminCommands(self.config)
        
        self.initialize_tts()

        if self.config["system_sound"]:
            winsound.Beep(800, 800)
    
    def initialize_tts(self):        
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            self.tts_engine.setProperty('voice', voices[self.config["voice"]].id)
            self.utility.handle_success("initialized", "TTS engine", voices[self.config["voice"]].id, show=False)
        except Exception as error:
            self.utility.handle_error("initializing TTS engine", error)
            self.tts_engine = None

    # NLP
    def preprocess_text(self, text):
        try:
            text = text.lower()
            text = text.strip()  # Remove leading and trailing white spaces
            text = re.sub(r'\s+', ' ', text)  # Multiple white spaces => single space
            text = re.sub(r'[^\w\s]', '', text)  # Remove non-word and non-space characters
            return text
        except Exception as error:
            self.utility.handle_error("text preprocessing", error)
            return text

    # Finding pattern (Not really)
    def match_pattern(self, user_message):
        try:
            for intent in self.admin_commands.intents:
                for pattern in intent["patterns"]:
                    if re.search(self.preprocess_text(pattern), user_message):
                        return intent
            return None
        except Exception as error:
            self.utility.handle_error("pattern matching", error)
            return None

    def update_unrecognized_file(self, user_message):
        try:
            # Checking if the unrecognized message already exists in the file
            df = pd.read_csv(self.config["unrecognized_file"], encoding="utf-8")
            existing_message = df[df["user_message"] == user_message]
            if existing_message.empty:
                # Adding a new unrecognized message entry
                new_entry = pd.DataFrame({
                    "count": [1],
                    "time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "user_message": [user_message]
                })
                new_entry.to_csv(self.config["unrecognized_file"], mode="a", header=False, index=False)
            else:
                # Updating count for the existing unrecognized message
                index = existing_message.index[0]
                df.at[index, "count"] += 1
                df.to_csv(self.config["unrecognized_file"], mode="w", header=True, index=False)
        except Exception as error:
            self.utility.handle_error("updating unrecognized file", error)

    def update_analize_data(self, id):
        try:
            df = pd.read_csv(self.config["analize_data_file"], encoding="utf-8")
            existing_entry = df[df["id"] == id]
            if existing_entry.empty:
                new_entry = pd.DataFrame({
                    "id": [id],
                    "count": [1]
                })
                new_entry.to_csv(self.config["analize_data_file"], mode="a", header=False, index=False)
            else:
                index = existing_entry.index[0]
                df.at[index, "count"] += 1
                df.to_csv(self.config["analize_data_file"], mode="w", header=True, index=False)
        except Exception as error:
            self.utility.handle_error("updating analyzing data file", error)

    def generate_response(self, user_message):
        try:
            user_message = self.preprocess_text(user_message)

            if not user_message:
                return "Please enter a valid message."

            # Offile Response
            intent = self.match_pattern(user_message)
            if intent and "responses" in intent:
                response_id = intent["id"]
                response = random.choice(intent["responses"])
                self.update_analize_data(response_id)
                self.utility.log_action(f'Chatbot responded to `{user_message}` with ({response_id}) `{response}`')
                return response

            # Searching wiki
            if user_message.startswith("what is"):
                response_text = self.wikipedia_search.wikipedia_search(user_message)
                return response_text

            self.update_unrecognized_file(user_message)
            self.utility.log_action(f'Chatbot failed to respond to `{user_message}`')
            return self.config["fallback_response"]

        except Exception as error:
            self.utility.handle_error("generating response", error)
            return None

    def speak(self, text):
        try:
            if self.config["speak_response"]:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as error:
            self.utility.handle_error("text-to-speech", error)

    def main(self):
        print(f"{TextStyle.fg['G']}Welcome to the chatbot! Type 'exit' to end the conversation.{TextStyle.fg['x']}")

        try:
            while True:
                user_message = input(f'{self.config["user_name"]}: ')
                if user_message.lower() == "exit" or user_message.lower() == "quit":
                    print(f"{TextStyle.fg['Y']}Chat ended{TextStyle.fg['x']}")
                    self.utility.log_action(f'Status change detected: stopped')
                    self.utility.close_log_file()
                    break

                # Handling admin commands
                elif user_message.lower().startswith(self.admin_commands.admin_prefix):
                    command = user_message.lower().replace(self.admin_commands.admin_prefix, "").strip()
                    self.admin_commands.handle_admin_command(command)
                    continue

                bot_reply = self.generate_response(user_message)
                print(f'{self.config["bot_name"]}: ' + bot_reply)
                self.speak(bot_reply)

        except Exception as error:
            self.utility.handle_error("main() loop", error)
        finally:
            if self.tts_engine is not None:
                self.tts_engine.stop()

if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        utility = Utility(config)
        utility.log_action("Status change detected: running")
        utility.log_action(f"Loaded Chatbot with configuration: {config}")

        chatbot = Chatbot(config)
        chatbot.main()
    except FileNotFoundError:
        utility.handle_file_not_found_error("Config", config_file)
    except Exception as error:
        utility.handle_error("booting", error)
