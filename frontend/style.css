import os
import json
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from waitress import serve
import uuid

# Load environment
load_dotenv()

# Initialize app
app = Flask(__name__)
CORS(app)

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config", "bluejay_config.json")
template_path = os.path.join(base_dir, "config", "conversation_template.json")

# Load brain
with open(config_path, "r") as f:
    brain = json.load(f)

# Load template
try:
    with open(template_path, "r") as tf:
        template = json.load(tf)
except:
    template = {}

# Redis setup
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url)

# OpenAI setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("OPENAI_ASSISTANT_ID", "asst_bLMfZI9fO9E5jltHY8KDq9ZT")

# Helper
def redis_key(thread_id):
    return f"thread:{thread_id}"

# Generate or reuse thread ID
def get_thread_id(request):
    thread_id = request.json.get("thread_id")
    if thread_id:
        return thread_id
    session_id = request.remote_addr or str(uuid.uuid4())
    return f"session:{session_id}"

# Chat route
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    thread_id = get_thread_id(request)
    key = redis_key(thread_id)

    # Load memory
    history = redis_client.get(key)
    thread_messages = json.loads(history) if history else []

    # Append user message
    thread_messages.append({"role": "user", "content": user_input})

    # System prompt
    system = {
        "role": "system",
        "content": f"You are BlueJay, a persuasive assistant. Use this brain:\n{json.dumps(brain)}\nUse this flow:\n{json.dumps(template)}"
    }

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[system] + thread_messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        thread_messages.append({"role": "assistant", "content": reply})
        redis_client.setex(key, 1800, json.dumps(thread_messages))
        return jsonify({"reply": reply, "thread_id": thread_id})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

@app.route("/")
def home():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
