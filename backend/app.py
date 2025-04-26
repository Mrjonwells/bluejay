import os
import time
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI()

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

assistant_id = os.getenv("ASSISTANT_ID")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    user_id = data.get("user_id")

    if not user_input or not user_id:
        return jsonify({"reply": "Missing input or session ID."}), 400

    thread_key = f"thread:{user_id}"
    thread_id = r.get(thread_key)

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id, ex=86400)

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    start_time = time.time()
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            return jsonify({"reply": "BlueJay encountered a problem."})
        elif time.time() - start_time > 100:
            return jsonify({"reply": "Response timeout. Please try again."})
        time.sleep(1)

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for m in reversed(messages.data):
        if m.role == "assistant":
            return jsonify({"reply": m.content[0].text.value})

    return jsonify({"reply": "No assistant reply found."})
