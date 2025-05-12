import os
import json
import redis
import openai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from waitress import serve

# Load environment
load_dotenv()

# Initialize Flask
app = Flask(__name__)
CORS(app)

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config", "bluejay_config.json")
template_path = os.path.join(base_dir, "config", "conversation_template.json")

# Load BlueJay brain
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

# Key builder
def redis_key(thread_id):
    return f"thread:{thread_id}"

# Routes
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    thread_id = data.get("thread_id", "default")

    # Load memory from Redis
    memory_key = redis_key(thread_id)
    history = redis_client.get(memory_key)
    thread_messages = json.loads(history) if history else []

    # Append user input to thread
    thread_messages.append({"role": "user", "content": user_input})

    # Inject system context
    system_prompt = {
        "role": "system",
        "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template:\n{json.dumps(template)}"
    }
    messages = [system_prompt] + thread_messages

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        thread_messages.append({"role": "assistant", "content": reply})
        redis_client.setex(memory_key, 1800, json.dumps(thread_messages))
        return jsonify({"reply": reply})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

@app.route("/")
def home():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
