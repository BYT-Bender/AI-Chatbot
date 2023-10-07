from datetime import datetime

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

    def handle_file_not_found_error(self, file_type, file_path):
        print(f"{TextStyle.fg['R']}Error: {file_type.title()} file not found (`{file_path}`){TextStyle.fg['x']}")
        self.log_action(f"Error: {file_type.title()} file not found (`{file_path}`)")

    def handle_error(self, action, error):
        print(f"{TextStyle.fg['R']}Error: Occurred during {action.lower()}: {error}{TextStyle.fg['x']}")
        self.log_action(f"Error: Occurred during {action.lower()}: {error}")

    def handle_success(self, action, file_type, file_path, show=True):
        if show:
            print(f"{TextStyle.fg['G']}{file_type.title()} file {action.lower()} successfully...{TextStyle.fg['x']}")
        self.log_action(f"Success: {action.capitalize()} {file_type} file (`{file_path}`)")
