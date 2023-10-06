# Copyright © 2023 BYT-Bender

import re
import pandas as pd
from datetime import datetime
from getpass import getpass
import pyttsx3
import winsound
import json
from formatting import TextStyle
import random
from wikipedia_search import WikipediaSearch
import requests
from bs4 import BeautifulSoup

# try:
#     import pyttsx3
#     print("module 'pyttsx3' is installed.")
# except ModuleNotFoundError:
#     print("module 'pyttsx3' is not installed.")

# try:
#     import winsound
#     print("module 'winsound' is installed.")
# except ModuleNotFoundError:
#     print("module 'winsound' is not installed.")

class Chatbot:
    # Initializing assest
    def __init__(self, config, wiki_search):
        self.config = config
        self.log_file = open(self.config["log_file"], 'a')
        self.log_action(f'Loaded Chatbot with configuration: {self.config}')
        self.load_assets()
        self.wiki_search = wiki_search

    def load_assets(self):
        try:
            self.initialize_tts()
            self.reload_responses()
            self.load_admin_commands()
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during initialization: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error during initialization: {error}')
            exit(1)

        if self.config["system_sound"]:
            winsound.Beep(800, 800)

    def log_action(self, action):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {action}\n'
        
        self.log_file.write(log_message)
        self.log_file.flush()
    
    def close_log_file(self):
        self.log_file.close()

    def reload_responses(self):
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
    
    def load_admin_commands(self):
        try:
            commands_df = pd.read_csv(self.config["commands_file"], encoding="utf-8")

            self.admin_commands = {}
            for index, row in commands_df.iterrows():
                command = row["command"]
                function = row["function"]
                arguments = row["arguments"]
                if not pd.isna(arguments):
                    arguments = [arg.strip() for arg in arguments.split(",") if arg.strip()]
                else:
                    arguments = []
                self.admin_commands[command] = {"function": function, "arguments": arguments}
            
            self.admin_password = commands_df["password"].values[0]
            self.admin_prefix = commands_df["prefix"].values[0]

            self.log_action(f'Successfully loaded Commands file ({self.config["commands_file"]})')
        except FileNotFoundError:
            print(f"{TextStyle.fg['R']}Error: Commands file not found.{TextStyle.fg['x']}")
            self.log_action(f'FileNotFoundError: Commands file ({self.config["commands_file"]})')
            raise
        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred while loading admin commands: {error}{TextStyle.fg['x']}")
            self.log_action(f'Failed to load Commands file ({self.config["commands_file"]})')
            raise
    
    def initialize_tts(self):        
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            self.tts_engine.setProperty('voice', voices[self.config["voice"]].id)
            self.log_action(f'Successfully initialized TTS engine')
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error initializing TTS engine: {error}{TextStyle.fg['x']}")
            self.log_action(f'Failed to initialize TTS engine')
            self.tts_engine = None

    # Reload assets while program is running
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
                
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during Chatbot reload: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error during Chatbot reload: {error}')

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
            self.log_action(f'Error during text preprocessing: {error}')
            return text

    # Finding pattern (Not really)
    def match_pattern(self, user_message):
        try:
            for intent in self.intents:
                for pattern in intent["patterns"]:
                    if re.search(self.preprocess_text(pattern), user_message):
                        return intent
            return None
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during pattern matching: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error during pattern matching: {error}')
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
            self.log_action(f'Error updating unrecognized file: {error}')

    def handle_admin_command(self, command):
        try:
            password = getpass(f"{TextStyle.fg['B']}Enter admin password: {TextStyle.fg['x']}")
            if password == self.admin_password:
                
                if command in self.admin_commands:
                    command_info = self.admin_commands[command]
                    function_name = command_info["function"]
                    arguments = command_info["arguments"]

                    if hasattr(self, function_name) and callable(getattr(self, function_name)):
                        function_to_execute = getattr(self, function_name)
                        function_to_execute(*arguments)
                    else:
                        print(f"{TextStyle.fg['Y']}Invalid command: Function not found.{TextStyle.fg['x']}")
                        self.log_action(f"Invalid command: Can't find instance of `{function_name}`")
                else:
                    print(f"{TextStyle.fg['Y']}Invalid command.{TextStyle.fg['x']}")
                    self.log_action(f'Invalid command: {command}')
            else:
                print(f"{TextStyle.fg['Y']}Invalid password.{TextStyle.fg['x']}")
                self.log_action(f'Invalid password.')
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
            print(f"{TextStyle.fg['R']}Error updating analyzing data file: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error updating analyzing data file: {error}')

    def generate_response(self, user_message):
        try:
            user_message = self.preprocess_text(user_message)

            # Offile Response
            intent = self.match_pattern(user_message)
            if intent and "responses" in intent:
                response_id = intent["id"]
                response = random.choice(intent["responses"])
                self.update_analize_data(response_id)
                self.log_action(f'Chatbot responded to `{user_message}` with ({response_id}) `{response}`')
                return response

            # Searching wiki
            if user_message.startswith("what is"):
                response_text = self.wikipedia_search(user_message)
                return response_text

            self.update_unrecognized_file(user_message)
            self.log_action(f'Chatbot failed to respond to `{user_message}`')
            return self.config["fallback_response"]

        except Exception as error:
            print(f"{TextStyle.fg['R']}Error generating response: {error}{TextStyle.fg['x']}")
            self.log_action(f"Error generating response: {error}")
            return None

    def wikipedia_search(self, user_message):
        try:
            # Extracting search query (after "What is")
            search_query = user_message[7:].strip()

            custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
            wikipedia_api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={search_query}&prop=extracts&exintro=1"

            # Making HTTP request
            headers = {"User-Agent": custom_user_agent}
            response = requests.get(wikipedia_api_url, headers=headers)
            data = response.json()

            # Extracting page content
            pages = data.get("query", {}).get("pages", {})
            page = next(iter(pages.values()), None)

            if page and "extract" in page:
                response_html = page["extract"]
                soup = BeautifulSoup(response_html, 'html.parser')
                
                # Allow only specified tags, and convert them to strings
                # allowed_tags = ['i', 'b', 'u']
                # for tag in soup.find_all(True):
                #     if tag.name not in allowed_tags:
                #         tag.unwrap()
                # cleaned_html = str(soup).strip()
                
                response_text = soup.select('p ~ p')[0].get_text().strip()
            else:
                response_text = "I couldn't find detailed information on that topic in Wikipedia."

            self.log_action(f'Chatbot responded to `{user_message}` with Wikipedia search result `{response_text}`')
            return response_text

        except Exception as error:
            print(f"{TextStyle.fg['R']}Error searching Wikipedia: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error searching Wikipedia: {error}')
            return None

    def speak(self, text):
        try:
            if self.config["speak_response"]:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
        except Exception as error:
            print(f"{TextStyle.fg['R']}Error during text-to-speech: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error during text-to-speech: {error}')

    def main(self):
        print(f"{TextStyle.fg['G']}Welcome to the chatbot! Type 'exit' to end the conversation.{TextStyle.fg['x']}")

        try:
            while True:
                user_message = input(f'{self.config["user_name"]}: ')
                if user_message.lower() == "exit" or user_message.lower() == "quit":
                    print(f"{TextStyle.fg['Y']}Chat ended{TextStyle.fg['x']}")
                    self.log_action(f'Status change detected: stopped')
                    chatbot.close_log_file()
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

        except Exception as error:
            print(f"{TextStyle.fg['R']}An error occurred: {error}{TextStyle.fg['x']}")
        finally:
            if self.tts_engine is not None:
                self.tts_engine.stop()

if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            config = json.load(config_file)

        wiki_search = WikipediaSearch({"User-Agent": config["user_agent"]})
        chatbot = Chatbot(config, wiki_search)
        
        chatbot.log_action("Status change detected: running")
        chatbot.main()
    except FileNotFoundError:
        print(f"{TextStyle.fg['R']}Error: Config file not found.{TextStyle.fg['x']}")
    except Exception as error:
        print(f"{TextStyle.fg['R']}An error occurred: {error}{TextStyle.fg['x']}")
