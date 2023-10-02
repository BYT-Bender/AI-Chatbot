import requests

class WikipediaSearch:
    def __init__(self, user_agent):
        self.user_agent = user_agent

    def search(self, search_query):
        try:
            # Use Wikipedia API to search for information with the custom user agent
            url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro=true&explaintext=true&titles={search_query}"
            response = requests.get(url, headers=self.user_agent)

            data = response.json()
            page = next(iter(data["query"]["pages"].values()))

            if "extract" in page:
                response_text = page["extract"]
                if response_text:
                    response = response_text.strip()
                else:
                    response = "I couldn't find detailed information on that topic in Wikipedia."
            else:
                response = "I couldn't find information on that topic."
            return response

        except Exception as error:
            print(f"Error searching Wikipedia: {error}")
            return "An error occurred while searching Wikipedia."
