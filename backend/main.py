import os
import json
import openai
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
from backend.utils.hubspot_helper import submit_lead_to_hubspot

# Load environment
load_dotenv()

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")

# Load brain config
with open(CONFIG_PATH, "r") as f:
    brain = json.load(f)

try:
    with open(TEMPLATE_PATH, "r") as tf:
        conversation_template = json.load(tf)
except:
    conversation_template = {}

# Flask app
app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

# Thread helpers
def redis_key(thread_id): return f"thread:{thread_id}"
def summarize_thread(messages):
    return " ".join([m["content"] for m in messages if m["role"] == "user"])[-1000:]

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id") or str(uuid.uuid4())
    user_input = data.get("message", "").strip()

    if not user_input:
        return jsonify({"reply": "I didn’t catch that — can you try again?"})

    # Load previous messages
    history = redis_client.get(redis_key(thread_id))
    thread_messages = json.loads(history) if history else []

    # Add user input
    thread_messages.append({"role": "user", "content": user_input})

    # AI call
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template if helpful:\n{json.dumps(conversation_template)}"},
            *thread_messages
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content
    thread_messages.append({"role": "assistant", "content": reply})
    redis_client.setex(redis_key(thread_id), 3600, json.dumps(thread_messages))  # 1 hour memory

    # Lead detection
    name = next((m["content"] for m in thread_messages if "my name is" in m["content"].lower()), "")
    email = next((m["content"] for m in thread_messages if "@" in m["content"]), "")
    phone = next((m["content"] for m in thread_messages if any(x in m["content"] for x in ["call", "text", "phone", "reach me at"])), "")

    if name and email and phone:
        summary = summarize_thread(thread_messages)
        submit_lead_to_hubspot(name, email, phone, summary)

    return jsonify({"reply": reply, "thread_id": thread_id})

@app.route("/")
def ping():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
