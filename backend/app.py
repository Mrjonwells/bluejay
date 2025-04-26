import os
import time
import redis
import requests
import re
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# Flask secret key
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
client = OpenAI(api_key=openai_api_key)

# Health check route for Render
@app.route("/health")
def health():
    return "OK", 200

# Static frontend (optional if needed)
@app.route("/<path:path>")
def static_file(path):
    return send_from_directory('frontend', path)

# Main chat route
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data or "user_id" not in data:
        return jsonify({"error": "Missing message or user_id"}), 400

    user_message = data["message"]
    user_id = data["user_id"]

    # Get or create a thread ID for this user
    thread_key = f"thread:{user_id}"
    thread_id = r.get(thread_key)

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id)

    # Add the message to the thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    # Poll until completion
    while run.status not in ["completed", "failed"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        return jsonify({"response": response})
    else:
        return jsonify({"error": "Assistant failed to generate a response."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)