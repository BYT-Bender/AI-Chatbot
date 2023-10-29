# Copyright © 2023 BYT-Bender

import json
from flask import Flask, request, jsonify, send_from_directory
from chatbot import Chatbot

# Create a Flask application
app = Flask(__name__, static_url_path="", static_folder="assets/server")

# Load the configuration from a JSON file
try:
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        config["log_file"] = config["log_files"]["web"]
except Exception as error:
    print(f"Error loading configuration: {str(error)}")

# Create an instance of the Chatbot class
chatbot = Chatbot(config)


# Define a route to handle incoming POST requests for processing user input
@app.route("/process", methods=["POST"])
def process():
    if request.method == "POST":
        data = request.form.get("user_input")
        if data:
            try:
                # Generate a response using the Chatbot
                response = chatbot.generate_response(data)
                return jsonify({"response": response})
            except Exception as error:
                return (jsonify({"error": f"Error processing request: {str(error)}"}), 500)
        else:
            return jsonify({"error": "Invalid input"}), 400


# Define a route to serve the index.html file
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    # Start the Flask application
    app.run()
