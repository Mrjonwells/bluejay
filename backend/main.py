import os
import json
import openai
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve

# Load environment variables
load_dotenv()

# Load config from correct absolute path
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")

# Load BlueJay brain
with open(CONFIG_PATH, "r") as f:
    brain = json.load(f)

# Load sales conversation template
try:
    with open(TEMPLATE_PATH, "r") as tf:
        conversation_template = json.load(tf)
except:
    conversation_template = {}

# Setup services
app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Helper to generate unique thread keys
def redis_key(thread_id): return f"thread:{thread_id}"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id") or str(uuid.uuid4())
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "What’s on your mind?"})

    # Retrieve history from Redis
    history = redis_client.get(redis_key(thread_id))
    thread_messages = json.loads(history) if history else []

    # Add user message
    thread_messages.append({"role": "user", "content": user_input})

    # OpenAI assistant call
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

    # Store updated history in Redis for 1 hour
    redis_client.setex(redis_key(thread_id), 3600, json.dumps(thread_messages))

    # Optional: clear memory if a lead is detected
    if any(trigger in reply.lower() for trigger in ["submitted", "sent to hubspot", "booked a time"]):
        redis_client.delete(redis_key(thread_id))

    return jsonify({"reply": reply, "thread_id": thread_id})

@app.route("/")
def health():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
