import sys
sys.path.append('.')

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

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=openai_api_key)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    user_id = data.get("user_id", str(uuid.uuid4()))

    # Redis key
    thread_key = f"thread:{user_id}"

    # Try to get existing thread ID
    thread_id = r.get(thread_key)
    if thread_id is None:
        # No thread, create new
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id)

    # Send user message
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input,
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    # Wait for run to complete
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        time.sleep(1)

    # Get assistant response
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    assistant_reply = ""
    for msg in messages.data:
        if msg.role == "assistant":
            assistant_reply = msg.content[0].text.value
            break

    return jsonify({"reply": assistant_reply})

@app.route("/", methods=["GET"])
def home():
    return "BlueJay Backend Running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)