import os
import sys
import re
import json

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_directory)

from utilities import Utility

class GetWordDefination:
    def __init__(self, config):
        self.config = config
        # self.utility = Utility(self.config)

    def extract_word(self, user_message):
        patterns = [
            r'what is (.+)',
            r'what is the meaning of (.+)',
            r'what does (.+) mean'
        ]

        for pattern in patterns:
            match = re.search(pattern, user_message)
            if match:
                word = match.group(1)
                return word
            
        return None
    
    def get_meaning(self, user_message):
        word = self.extract_word(user_message)

        with open('D:/Files/Python/AI/CURRENT_VER/assets/responses/dictionary/dictionary.json', 'r') as json_file:
            dictionary = json.load(json_file)
        
        return dictionary.get(word)


    def generate_response(self, user_message):
        response = self.get_meaning(user_message)
        
        if response is not None:
            return response, "dictionary"
        else:
            return None, None