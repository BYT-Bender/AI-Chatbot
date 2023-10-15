# Copyright © 2023 BYT-Bender

import json
from datetime import datetime
import winsound

import pyttsx3
import pandas as pd
import signal

from assets.utilities import Utility
from assets.formatting import TextStyle
from assets.admin_commands import AdminCommands
from assets.responses.conversation.search_conversation import SearchConversation
from assets.responses.elements.search_element import SearchElement
from assets.responses.wikipedia.search_wikipedia import SearchWikipedia

class Chatbot:
    # Initializing assest
    def __init__(self, config):
        self.config = config
        
        self.utility = Utility(self.config)
        self.wikipedia_search = SearchWikipedia(self.config)
        self.conversation_search = SearchConversation(self.config)
        self.admin_commands = AdminCommands(self.config)
        self.search_element = SearchElement(self.config)
        
        self.initialize_tts()

        if self.config["system_sound"]:
            winsound.Beep(800, 800)

        signal.signal(signal.SIGINT, self.utility.handle_keyboard_interrupt)    

    def initialize_tts(self):        
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            self.tts_engine.setProperty('voice', voices[self.config["voice"]].id)
            self.utility.handle_success("initialized", "TTS engine", voices[self.config["voice"]].id, show=False)
        except Exception as error:
            self.utility.handle_error("initializing TTS engine", error)
            self.tts_engine = None

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

    def generate_response(self, user_message):
        try:
            user_message = self.utility.preprocess_text(user_message)

            if not user_message:
                return "Please enter a valid message."
            
            response_generators = [
                self.conversation_search, # Offile Response
                self.search_element, # Element Search
                self.wikipedia_search # Searching wiki
            ]

            for generator in response_generators:
                response = generator.generate_response(user_message)
                if response:
                    return response

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
        print(f"{TextStyle.fg['G']}Welcome to the chatbot! Type 'Ctrl + C' to end the conversation.{TextStyle.fg['x']}")

        try:
            while True:
                user_message = input(f'{self.config["user_name"]}: ')

                # Handling admin commands
                if user_message.lower().startswith(self.admin_commands.admin_prefix):
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

def load_config(config_file):
    try:
        with open(config_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise Exception(f"Config file '{config_file}' not found.")
    except Exception as error:
        raise Exception(f"Error loading configuration: {error}")

if __name__ == "__main__":
    try:
        config_file = "config.json"
        config = load_config(config_file)

        utility = Utility(config)
        utility.log_action("Status change detected: running")
        utility.log_action(f"Loaded Chatbot with configuration: {config}")

        chatbot = Chatbot(config)
        chatbot.main()

    except FileNotFoundError:
        utility.handle_file_not_found_error("Config", config_file)
    except Exception as error:
        utility.handle_error("booting", error)
