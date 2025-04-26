import os
import time
import redis
import requests
import re
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis Setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# OpenAI Setup
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

assistant_id = os.getenv("ASSISTANT_ID")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "BlueJay server is alive"}), 200

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('message', '')
        user_id = request.json.get('user_id', str(uuid.uuid4()))

        thread_key = f"thread:{user_id}"

        # Get existing thread ID
        thread_id = r.get(thread_key)

        if thread_id:
            thread_id = thread_id.decode('utf-8')
        else:
            # Create new thread
            thread = client.beta.threads.create()
            thread_id = thread.id
            r.set(thread_key, thread_id)

        # Post user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for completion
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run_status.status == 'completed':
                break
            time.sleep(1)

        # Get latest assistant message
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for message in messages.data:
            if message.role == 'assistant':
                return jsonify({'response': message.content[0].text.value})

        return jsonify({'response': "I'm here to help!"})

    except Exception as e:
        print(f"Error in /chat: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)