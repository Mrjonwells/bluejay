import os
import json
import openai
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve

# Load environment
load_dotenv()

# Load config from correct absolute path
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")

# Safety check for config
if not os.path.exists(CONFIG_PATH):
    raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")

with open(CONFIG_PATH, "r") as f:
    brain = json.load(f)

# Setup services
app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
redis_client = redis.from_url(os.getenv("REDIS_URL"))

def redis_key(thread_id): return f"thread:{thread_id}"

# Optional template
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")
try:
    with open(TEMPLATE_PATH, "r") as tf:
        conversation_template = json.load(tf)
except:
    conversation_template = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id", "default")
    user_input = data["message"]

    print(f"Received message from user: {user_input}")  # DEBUG LINE

    # Load prior messages
    history = redis_client.get(redis_key(thread_id))
    thread_messages = json.loads(history) if history else []
    thread_messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template if helpful:\n{json.dumps(conversation_template)}"},
            *thread_messages
        ],
        temperature=0.7
    )

    reply = response.choices[0].message["content"]
    thread_messages.append({"role": "assistant", "content": reply})
    redis_client.setex(redis_key(thread_id), 1800, json.dumps(thread_messages))

    return jsonify({"reply": reply})

@app.route("/")
def ping():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
