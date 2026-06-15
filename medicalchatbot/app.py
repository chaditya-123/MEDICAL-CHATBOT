from flask import Flask, render_template, request
import json
import random

app = Flask(__name__)

with open('intents.json', 'r') as file:
    data = json.load(file)

def chatbot_response(user_input):

    user_words = user_input.lower().split()

    best_match = None
    max_score = 0

    for intent in data['intents']:

        score = 0

        for pattern in intent['patterns']:

            pattern_words = pattern.lower().split()

            common_words = set(user_words).intersection(set(pattern_words))

            score += len(common_words)

        if score > max_score:
            max_score = score
            best_match = intent

    if best_match and max_score > 0:
        return random.choice(best_match['responses'])

    return "Sorry, I couldn't understand. Please describe your symptoms more clearly."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get')
def get_bot_response():

    user_text = request.args.get('msg')

    if not user_text:
        return "Please enter a symptom."

    return chatbot_response(user_text)

if __name__ == "__main__":
    app.run(debug=True)