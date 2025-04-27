import os
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
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("ASSISTANT_ID")

def get_thread_id(user_id):
    thread_key = f"thread:{user_id}"
    thread_id = r.get(thread_key)
    if thread_id:
        return thread_id.decode("utf-8")
    else:
        return None

def save_thread_id(user_id, thread_id):
    thread_key = f"thread:{user_id}"
    r.set(thread_key, thread_id)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400

    user_id = data.get("user_id", str(uuid.uuid4()))
    thread_id = get_thread_id(user_id)

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        save_thread_id(user_id, thread_id)

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    while True:
        run_check = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        if run_check.status == "completed":
            break

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    latest_message = messages.data[0].content[0].text.value

    return jsonify({"response": latest_message})

# --- VERY IMPORTANT --- dynamic PORT binding for Railway:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)