import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Environment Variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
redis_url = os.getenv("REDIS_URL")
flask_secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# Redis setup
r = redis.from_url(redis_url)

# OpenAI setup
client = OpenAI(api_key=openai_api_key)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    user_id = data.get("user_id")

    if not user_message or not user_id:
        return jsonify({"error": "Invalid request"}), 400

    # Manage user session
    thread_key = f"thread:{user_id}"
    thread_id = r.get(thread_key)

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        r.set(thread_key, thread_id)

    # Send user message
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_message
    )

    # Run assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Continue conversation smoothly as a merchant savings expert."
    )

    # Poll for completion
    while True:
        status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if status.status in ["completed", "failed", "cancelled"]:
            break

    if status.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        for msg in messages.data:
            if msg.role == "assistant":
                return jsonify({"response": msg.content[0].text.value})

    return jsonify({"error": "Failed to get assistant response"}), 500

@app.route("/", methods=["GET"])
def home():
    return "BlueJay server is running!"

if __name__ == "__main__":
    app.secret_key = flask_secret_key
    app.run(host="0.0.0.0", port=10000)