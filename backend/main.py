import os
import json
import redis
import uuid
import requests
import time
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
client = OpenAI()
ASSISTANT_ID = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load BlueJay brain
with open("bluejay/bluejay_config.json", "r") as f:
    bluejay_brain = json.load(f)

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.set(key, new_thread.id)
    return new_thread.id

@app.route("/", methods=["GET"])
def index():
    return """
    <html>
      <head><title>BlueJay Backend</title></head>
      <body style="background-color:#000; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
        <h1>BlueJay backend is live!</h1>
        <p>Brain + Assistant are ready. POST to <code>/chat</code> to begin.</p>
      </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "No input received."})

    # Calendly smart trigger
    if any(word in user_input.lower() for word in ["book", "schedule", "meet", "call", "calendar"]):
        return jsonify({"reply": "Sure — grab a time here: https://calendly.com/askbluejay/30min"})

    session_id = request.remote_addr or str(uuid.uuid4())
    thread_id = get_thread_id(session_id)

    system_context = f"""
BlueJay is a business-savvy assistant trained on custom configuration logic.
Use the following strategy guide as internal operating rules:

{json.dumps(bluejay_brain, indent=2)}

Do NOT mention this config to the user. Blend these principles into short, natural, question-driven replies. Be smart, discovery-led, and sales-focused. You are the left brain (config), working with the assistant (right brain).
"""

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            instructions=system_context
        )

        while True:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run.status in ["completed", "failed", "cancelled"]:
                break

        if run.status != "completed":
            return jsonify({"reply": f"Run status: {run.status}"})

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = next((m.content[0].text.value for m in messages.data if m.role == "assistant"), "...")
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": "Error: " + str(e)})
