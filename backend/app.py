import os
import uuid
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

r = redis.Redis.from_url(os.getenv("REDIS_URL"))
client = OpenAI()

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_id = data.get("user_id") or str(uuid.uuid4())
    message = data.get("message")

    thread_key = f"thread:{user_id}"

    thread_id = r.get(thread_key)
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.setex(thread_key, 1800, thread_id)  # 30-minute expiration
    else:
        r.expire(thread_key, 1800)  # Refresh TTL on every message

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
    )

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    latest_reply = next((m for m in reversed(messages.data) if m.role == "assistant"), None)

    return jsonify({"reply": latest_reply.content[0].text.value})

@app.route("/inspect", methods=["GET"])
def inspect():
    keys = r.keys("thread:*")
    active_threads = []
    for key in keys:
        ttl = r.ttl(key)
        value = r.get(key)
        active_threads.append({
            "key": key.decode(),
            "ttl": ttl,
            "thread_id": value.decode() if value else "None"
        })
    return jsonify(active_threads)