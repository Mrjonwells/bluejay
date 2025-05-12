import os
import json
import openai
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
import uuid

# Load environment variables
load_dotenv()

# Set up file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")

# Load BlueJay's brain
with open(CONFIG_PATH, "r") as f:
    brain = json.load(f)

# Load sales conversation template
try:
    with open(TEMPLATE_PATH, "r") as f:
        conversation_template = json.load(f)
except:
    conversation_template = {}

# Flask setup
app = Flask(__name__)
CORS(app)

# API and Redis setup
openai.api_key = os.getenv("OPENAI_API_KEY")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Helper to manage thread keys
def redis_key(thread_id): return f"thread:{thread_id}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    thread_id = data.get("thread_id") or str(uuid.uuid4())  # autogenerate if none

    # Retrieve conversation history
    history_json = redis_client.get(redis_key(thread_id))
    thread_messages = json.loads(history_json) if history_json else []

    # Add user message
    thread_messages.append({"role": "user", "content": user_input})

    # Assistant call
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template if helpful:\n{json.dumps(conversation_template)}"},
            *thread_messages
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()
    thread_messages.append({"role": "assistant", "content": reply})

    # Store updated conversation (30 min expiration)
    redis_client.setex(redis_key(thread_id), 1800, json.dumps(thread_messages))

    return jsonify({"reply": reply, "thread_id": thread_id})

@app.route("/")
def ping():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
