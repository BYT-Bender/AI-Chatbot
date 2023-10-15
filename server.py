import json

from flask import Flask, request, jsonify, send_from_directory

from chatbot import Chatbot

app = Flask(__name__, static_url_path='', static_folder='assets/server')

try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
except Exception as error:
    print(f'Error loading configuration: {str(error)}')
    config = {}

chatbot = Chatbot(config)

@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        data = request.form.get('user_input')
        if data:
            try:
                response = chatbot.generate_response(data)
                return jsonify({'response': response})
            except Exception as error:
                return jsonify({'error': f'Error processing request: {str(error)}'}), 500
        else:
            return jsonify({'error': 'Invalid input'}), 400

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run()
