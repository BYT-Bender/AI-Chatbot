import os
import sys
import re
import random

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_directory)

from utilities import Utility
from admin_commands import AdminCommands

class SearchConversation:
    def __init__(self, config):
        self.config = config
        self.utility = Utility(self.config)
        self.admin_commands = AdminCommands(self.config)

    def match_pattern(self, user_message):
        try:
            for intent in self.admin_commands.intents:
                for pattern in intent["patterns"]:
                    if re.search(self.utility.preprocess_text(pattern), user_message):
                        return intent
        except Exception as error:
            self.utility.handle_error("pattern matching", error)
        return None
        
    def generate_response(self, user_message):
        intent = self.match_pattern(user_message)
        if intent and "responses" in intent:
            response_id = intent["id"]
            response = random.choice(intent["responses"])
            self.utility.log_action(f'Chatbot responded to `{user_message}` with ({response_id}) `{response}`')
            self.utility.update_usage(self.config["conversation_response_usage"], response_id, "updating response usage data")
            return response, "conversation"
        else:
            return None, None
        
