import os
import requests

from flask import Flask, request

app = Flask(__name__)

# Store last message (in memory)
last_message = "No messages yet."

@app.route('/', methods=['GET'])
def home():
    return f"""
    <html>
        <body>
            <h1>Last GroupMe Message</h1>
            <p>{last_message}</p>
        </body>
    </html>
    """

@app.route('/', methods=['POST'])
def receive():
    global last_message
    data = request.get_json()

    print("Incoming message:")
    print(data)

    # Prevent self-reply
    if data.get('sender_type') != 'bot':
        last_message = f"{data.get('name')}: {data.get('text')}"

    # Prevent self-reply
    if data['sender_type'] != 'bot':
        if data['text'].startswith('/ping'):
            send(data['name'] + ' pinged me!')

    return 'ok', 200


def send(msg):
    print("BOT_ID:", os.getenv("BOT_ID"))
    url = 'https://api.groupme.com/v3/bots/post'
    payload = {
        'bot_id': os.getenv('BOT_ID'),
        'text': msg,
    }

    r = requests.post(url, json=payload)
    print("Send status:", r.status_code)
    print("Send response:", r.text)
