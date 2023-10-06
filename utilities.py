from datetime import datetime

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