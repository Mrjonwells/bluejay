import os
import uuid
import redis
import openai
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis setup
redis_url = os.getenv('REDIS_URL')
r = redis.Redis.from_url(redis_url)

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')
    user_id = data.get('user_id')

    if not user_message or not user_id:
        return jsonify({'error': 'Missing message or user_id'}), 400

    thread_key = f"thread:{user_id}"

    # Get or create a thread ID
    thread_id = r.get(thread_key)
    if thread_id is None:
        thread = openai.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id)
    else:
        thread_id = thread_id.decode()

    # Send the user message
    openai.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Run the assistant
    run = openai.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Polling until run completes
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if run_status.status == 'completed':
            break
        elif run_status.status == 'failed':
            return jsonify({'error': 'Assistant run failed'}), 500
        time.sleep(1)

    # Get the assistant's reply
    messages = openai.beta.threads.messages.list(thread_id=thread_id)
    last_message = messages.data[0]

    assistant_reply = last_message.content[0].text.value

    return jsonify({'assistant': assistant_reply})

@app.route('/', methods=['GET'])
def home():
    return "BlueJay backend is live."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)