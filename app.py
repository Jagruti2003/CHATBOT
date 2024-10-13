from flask import Flask, render_template, request, jsonify, send_from_directory
import json
import random
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

def load_intents():
    with open('intents.json', 'r', encoding='utf-8') as file:
        return json.load(file)

intents = load_intents()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message'].lower()
    
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_message:
                return jsonify({'response': random.choice(intent['responses'])})
    
    return jsonify({'response': "I'm not sure about that. Can you ask something else?"})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)