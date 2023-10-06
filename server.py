from flask import Flask, request, jsonify
from chatbot import Chatbot
from flask import send_from_directory
from wikipedia_search import WikipediaSearch
import json

app = Flask(__name__, static_url_path='', static_folder='assets')

with open("config.json", "r") as config_file:
    config = json.load(config_file)

wiki_search = WikipediaSearch({"User-Agent": config["user_agent"]})
chatbot = Chatbot(config, wiki_search)

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        data = request.form.get('user_input')  # Get the user input from the AJAX request
        response = chatbot.generate_response(data)  # Generate the response using the Chatbot class
        return jsonify({'response': response})  # Return the response as JSON

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run()
