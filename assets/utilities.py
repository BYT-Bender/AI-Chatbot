import sys
from datetime import datetime
import json
import re
import os
import pandas as pd

sys.path.append(os.path.dirname(__file__))
from formatting import TextStyle

class Utility:
    def __init__(self, config):
        self.config = config
        self.log_file = open(self.config["log_file"], 'a')

    def log_action(self, action):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f'[{timestamp}] {action}\n'
        
        self.log_file.write(log_message)
        self.log_file.flush()
    
    def close_log_file(self):
        self.log_file.close()

    def load_json(self, file_name, file_path, show=True):
        try:
            with open(file_path, "r") as file:
                self.handle_success("Loaded", file_name, file_path, show)
                return json.load(file)
            
        except FileNotFoundError:
            self.handle_file_not_found_error(file_name, file_path)
            
        except Exception as error:
            self.handle_error(f"Loading {file_name}", error)
        
    def handle_command_use(self, command, function_name, arguments):
        self.log_action(f"Admin Command Used: `{command}` which triggered function `{function_name}` with arguments {arguments}")

    def handle_invalid_command(self, command):
        print(f"{TextStyle.fg['R']}Error: Invalid command `{command}`{TextStyle.fg['x']}")
        self.log_action(f"Error: Invalid command `{command}`")

    def handle_invalid_function(self, command, function_name):
        print(f"{TextStyle.fg['R']}Error: Can't find instance of function `{function_name}`{TextStyle.fg['x']}")
        self.log_action(f"Error: Can't find instance of function `{function_name}` on command `{command}`")

    def handle_invalid_password(self):
        print(f"{TextStyle.fg['R']}Error: Invalid password{TextStyle.fg['x']}")
        self.log_action("Error: Invalid password")

    def handle_file_not_found_error(self, file_name, file_path):
        print(f"{TextStyle.fg['R']}Error: {file_name.title()} file not found (`{file_path}`){TextStyle.fg['x']}")
        self.log_action(f"Error: {file_name.title()} file not found (`{file_path}`)")

    def handle_error(self, action, error):
        print(f"{TextStyle.fg['R']}Error: Occurred during {action.lower()}: {error}{TextStyle.fg['x']}")
        self.log_action(f"Error: Occurred during {action.lower()}: {error}")

    def handle_success(self, action, file_name, file_path, show=True):
        if show:
            print(f"{TextStyle.fg['G']}{file_name.title()} file {action.lower()} successfully...{TextStyle.fg['x']}")
        self.log_action(f"Success: {action.capitalize()} {file_name} file (`{file_path}`)")

    def update_usage(self, file, id, error_msg):
        try:
            df = pd.read_csv(file, encoding="utf-8")
            existing_entry = df[df["id"] == id]
            if existing_entry.empty:
                new_entry = pd.DataFrame({
                    "id": [id],
                    "count": [1]
                })
                new_entry.to_csv(file, mode="a", header=False, index=False)
            else:
                index = existing_entry.index[0]
                df.at[index, "count"] += 1
                df.to_csv(file, mode="w", header=True, index=False)
        except Exception as error:
            self.handle_error(error_msg, error)

    def update_time_usage(self, file, response_type, error_msg):
        try:
            df = pd.read_csv(file, encoding="utf-8")

            today_date = datetime.now().strftime('%Y-%m-%d')
            existing_entry = df[(df['date'] == today_date) & (df['response_type'] == response_type)]

            if existing_entry.empty:
                new_entry = pd.DataFrame({
                    "date": [today_date],
                    "response_type": [response_type],
                    "count": [1]
                })
                df = pd.concat([df, new_entry])
                # df = df.append(new_entry, ignore_index=True)
            else:
                index = existing_entry.index[0]
                df.at[index, "count"] += 1

            df.to_csv(file, mode="w", header=True, index=False)

        except Exception as error:
            self.handle_error(error_msg, error)
        
    def preprocess_text(self, text):
        try:
            text = text.lower()
            text = text.strip()  # Remove leading and trailing white spaces
            text = re.sub(r'\s+', ' ', text)  # Multiple white spaces => single space
            text = re.sub(r'[^\w\s]', '', text)  # Remove non-word and non-space characters
            return text
        except Exception as error:
            self.handle_error("text preprocessing", error)
            return text
        
    def handle_keyboard_interrupt(self, signal, frame):
        self.log_action(f'Keyboard interrupt with signal {signal} at frame {frame}')
        self.exit()

    def exit(self):
        print(f"{TextStyle.fg['Y']}Chat ended{TextStyle.fg['x']}")
        self.log_action(f'Status change detected: stopped')
        self.close_log_file()
        sys.exit(0)
