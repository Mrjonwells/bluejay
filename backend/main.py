import os
import uuid
import redis
import json
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

# Load BlueJay brain
with open("bluejay_config.json") as f:
    config = json.load(f)

def get_memory(thread_id):
    key = f"thread:{thread_id}"
    messages = r.lrange(key, 0, -1)
    return [json.loads(m.decode()) for m in messages]

def save_memory(thread_id, role, content):
    key = f"thread:{thread_id}"
    msg = {"role": role, "content": content, "timestamp": time.time()}
    r.rpush(key, json.dumps(msg))
    r.expire(key, 600)  # 10 min memory

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"reply": "I didn’t catch that. Can you rephrase?"})

    thread_id = data.get("thread_id") or str(uuid.uuid4())
    memory = get_memory(thread_id)

    messages = [{"role": "system", "content": config["system_prompt"]}]
    for m in memory:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=config.get("temperature", 0.7),
            max_tokens=500
        )
        reply = response.choices[0].message.content.strip()
        save_memory(thread_id, "user", message)
        save_memory(thread_id, "assistant", reply)
        return jsonify({"reply": reply, "thread_id": thread_id})
    except Exception as e:
        return jsonify({"reply": "There was an error. Please try again.", "error": str(e)}), 500

@app.route("/")
def index():
    return "BlueJay backend is live."

if __name__ == "__main__":
    app.run(debug=True)
