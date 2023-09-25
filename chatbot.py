# Copyright © 2023 Sourabh Srivastva

import re
import pandas as pd
from datetime import datetime
from getpass import getpass
import pyttsx3
import winsound
import json
from intents_data import intents
from formatting import TextStyle

class Chatbot:
    # Initializing assest
    def __init__(self, config):
        self.config = config
        self.initialize_tts()

        try:
            self.reload_responses()
            self.load_admin_commands()
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during initialization: {error}{TextStyle.fg['x']}")
            exit(1)

        if self.config["system_sound"]:
            winsound.Beep(800, 800)

    def reload_responses(self):
        try:
            self.responses = pd.read_csv(self.config["response_file"], encoding="utf-8")
        except FileNotFoundError:
            print(f"{TextStyle.fg['R']}Error: Response file not found.{TextStyle.fg['x']}")
            raise
        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred while loading responses: {error}{TextStyle.fg['x']}")
            raise
    
    def load_admin_commands(self):
        try:
            commands_df = pd.read_csv(self.config["commands_file"], encoding="utf-8")
            # self.admin_commands = dict(zip(commands_df["command"], commands_df["function"]))
            self.admin_commands = commands_df["command"].values.tolist()
            self.admin_password = commands_df["password"].values[0]
            self.admin_prefix = commands_df["prefix"].values[0]
        except FileNotFoundError:
            print(f"{TextStyle.fg['R']}Error: Commands file not found.{TextStyle.fg['x']}")
            raise
        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred while loading admin commands: {error}{TextStyle.fg['x']}")
            raise
    
    def initialize_tts(self):        
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            self.tts_engine.setProperty('voice', voices[self.config["voice"]].id)
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error initializing TTS engine: {error}{TextStyle.fg['x']}")
            self.tts_engine = None

    # Reload assests while program is running
    def reload_chatbot(self, reload_responses=True, reload_admin_commands=True):
        try:
            if reload_responses:
                self.reload_responses()
                print(f"{TextStyle.fg['G']}Responses reloaded successfully...{TextStyle.fg['x']}")

            if reload_admin_commands:
                self.load_admin_commands()
                print(f"{TextStyle.fg['G']}Admin Commands reloaded successfully...{TextStyle.fg['x']}")

            if self.config["system_sound"]:
                winsound.Beep(1000, 500)

            # print("Chatbot successfully reloaded!")
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during chatbot reload: {error}{TextStyle.fg['x']}")

    # NLP
    def preprocess_text(self, text):
        try:
            text = text.lower()
            text = text.strip()  # Remove leading and trailing white spaces
            text = re.sub(r'\s+', ' ', text)  # Multiple white spaces => single space
            text = re.sub(r'[^\w\s]', '', text)  # Remove non-word and non-space characters
            return text
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during text preprocessing: {error}{TextStyle.fg['x']}")
            return text

    # intents dictionary => DataFrame
    patterns_data = []
    for intent_id, intent_data in intents.items():
        for phrase in intent_data["phrases"]:
            patterns_data.append([intent_id, phrase])
    patterns_df = pd.DataFrame(patterns_data, columns=["intent_id", "pattern"])

    # Finding pattern (Not really)
    def match_pattern(self, user_message):
        try:
            for _, row in self.patterns_df.iterrows():
                pattern = row["pattern"]
                intent_id = row["intent_id"]
                if re.search(self.preprocess_text(pattern), user_message):
                    return intent_id
            return None
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during pattern matching: {error}{TextStyle.fg['x']}")
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
            print(f"{TextStyle.fg['R']}Error updating unrecognized file: {error}{TextStyle.fg['x']}")

    def handle_admin_command(self, command):
        try:
            password = getpass(f"{TextStyle.fg['B']}Enter admin password: {TextStyle.fg['x']}")
            if password == self.admin_password:
                if command == self.admin_commands[0]:
                    self.clear_responses()
                elif command == self.admin_commands[1]:
                    self.clear_unrecognized()
                else:
                    print(f"{TextStyle.fg['Y']}Invalid command.{TextStyle.fg['x']}")
            else:
                print(f"{TextStyle.fg['Y']}Invalid password.{TextStyle.fg['x']}")
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error handling admin command: {error}{TextStyle.fg['x']}")

    # def clear_patterns(self):
    #     self.clear_file(self.pattern_file, ["response_id", "pattern"], "Patterns")

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
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error clearing {name.lower()}: {error}{TextStyle.fg['x']}")
        
    def generate_response(self, user_message):
        try:
            user_message = self.preprocess_text(user_message)
            intent_id = self.match_pattern(user_message)
            if intent_id is not None:
                matched_response = self.responses.loc[self.responses["response_id"] == intent_id]
                if not matched_response.empty:
                    return matched_response["bot_response"].values[0]

            self.update_unrecognized_file(user_message)
            return "I'm sorry, I don't understand. Can you please rephrase?"
        except Exception as error:
            # print(f"{TextStyle.fg['R']}An error occurred while generating a response.{TextStyle.fg['x']}")
            print(f"{TextStyle.fg['R']}Error generating response: {error}{TextStyle.fg['x']}")
            return None

    def speak(self, text):
        try:
            if self.config["speak_response"]:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during text-to-speech: {error}{TextStyle.fg['x']}")

    def main(self):
        print(f"{TextStyle.fg['G']}Welcome to the chatbot! Type 'exit' to end the conversation.{TextStyle.fg['x']}")
        self.load_admin_commands()

        try:
            while True:
                user_message = input(f'{self.config["user_name"]}: ')
                if user_message.lower() == "exit" or user_message.lower() == "quit":
                    print(f"{TextStyle.fg['Y']}Chat ended{TextStyle.fg['x']}")
                    break

                # Handling reload commands
                elif user_message.lower().startswith("reload"):
                    command = user_message.lower().replace("reload", "").strip()
                    if command == "all" or command == "":
                        self.reload_chatbot(reload_responses=True, reload_admin_commands=True)
                    elif command == "responses":
                        self.reload_chatbot(reload_responses=True, reload_admin_commands=False)
                    elif command == "admin commands":
                        self.reload_chatbot(reload_responses=False, reload_admin_commands=True)
                    else:
                        print("Invalid reload command.")
                    continue

                # Handling admin commands
                elif user_message.lower().startswith(self.admin_prefix):
                    command = user_message.lower().replace(self.admin_prefix, "").strip()
                    self.handle_admin_command(command)
                    continue

                bot_reply = self.generate_response(user_message)
                print(f'{self.config["bot_name"]}: ' + bot_reply)
                self.speak(bot_reply)

        except Exception as e:
            print(f"{TextStyle.fg['R']}An error occurred: {e}{TextStyle.fg['x']}")
        finally:
            if self.tts_engine is not None:
                self.tts_engine.stop()


if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        chatbot = Chatbot(config)
        chatbot.main()
    except FileNotFoundError:
        print(f"{TextStyle.fg['R']}Error: Config file not found.{TextStyle.fg['x']}")
    except Exception as error:
        print(f"{TextStyle.fg['R']}An error occurred: {error}{TextStyle.fg['x']}")
