import requests
from bs4 import BeautifulSoup

from formatting import TextStyle
from utilities import Utility

class WikipediaSearch:
    def __init__(self, config):
        self.config = config
        self.log_action = Utility(self.config).log_action
        self.user_agent = self.config["user_agent"]

    def is_internet_available(self):
        try:
            response = requests.get("https://www.google.com")
            return response.status_code == 200
        except requests.RequestException:
            return False

    def wikipedia_search(self, user_message):
        try:
            if not self.is_internet_available():
                return "Sorry, I couldn't connect to the internet."
            
            # Extracting search query (after "What is")
            search_query = user_message[7:].strip()

            wikipedia_api_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&titles={search_query}&prop=extracts&exintro=1"

            # Making HTTP request
            headers = {"User-Agent": self.user_agent}
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

        except requests.RequestException as error:
            print(f"{TextStyle.fg['R']}Error connecting to the internet: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error connecting to the internet: {error}')

        except Exception as error:
            print(f"{TextStyle.fg['R']}Error searching Wikipedia: {error}{TextStyle.fg['x']}")
            self.log_action(f'Error searching Wikipedia: {error}')
            return None
