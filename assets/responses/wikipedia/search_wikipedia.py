import os
import sys

import requests
from bs4 import BeautifulSoup

parent_directory = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(parent_directory)

from utilities import Utility

class SearchWikipedia:
    def __init__(self, config):
        self.config = config
        self.utility = Utility(self.config)
        self.user_agent = self.config["user_agent"]

    def is_internet_available(self):
        try:
            response = requests.get("https://www.google.com")
            return response.status_code == 200
        except requests.RequestException as error:
            self.utility.log_action(f'Error: While connecting to the internet: {error}')
            return False

    def wikipedia_search(self, user_message):
        try:            
            # Extracting search query (after "What is")
            search_query = user_message[7:].strip()
            wikipedia_api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={search_query}&prop=extracts&exintro=1"

            # Making an HTTP request to Wikipedia.
            headers = {"User-Agent": self.user_agent}
            response = requests.get(wikipedia_api_url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors.

            data = response.json()
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
                
                # Extract and clean the page content.
                response_text = soup.select('p ~ p')[0].get_text().strip()
                self.utility.log_action(f'Chatbot responded to `{user_message}` with Wikipedia search result `{response_text}`')
                return response_text
            else:
                return None
            
        except requests.RequestException as error:
            self.utility.log_action(f'Error: While connecting to Wikipedia: {error}')
            return None

        except Exception as error:
            self.utility.log_action(f'Error: While searching Wikipedia: {error}')
            return None
        

    def generate_response(self, user_message):
        if user_message.startswith("what is") and self.is_internet_available():
            response = self.wikipedia_search(user_message)
            return response
        else:
            return None