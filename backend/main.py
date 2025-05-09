import os
import json
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# Load config once at startup
CONFIG_PATH = "backend/config/bluejay_config.json"
with open(CONFIG_PATH, "r") as f:
    bluejay_config = json.load(f)

# OpenAI setup
client = OpenAI()
assistant_id = os.getenv("ASSISTANT_ID")

# Flask app
app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    thread_id = data.get("thread_id")
    message = data.get("message")

    if not thread_id or not message:
        return jsonify({"error": "Missing thread_id or message"}), 400

    # Save message in Redis
    key = f"thread:{thread_id}"
    thread_data = json.loads(r.get(key)) if r.get(key) else {"messages": []}
    thread_data["messages"].append({"role": "user", "content": message})
    r.setex(key, 1800, json.dumps(thread_data))  # 30 min TTL
    r.expire(key, 1800)  # Refresh TTL on access

    # Send message to OpenAI Assistant with streaming
    stream = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Use bluejay_config to guide behavior.",
    )

    # Poll run status
    while True:
        run_check = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        if run_check.status == "completed":
            break
        elif run_check.status == "failed":
            return jsonify({"error": "Assistant run failed"}), 500

    messages = client.beta.threads.messages.list(thread_id=thread_id)
    latest = messages.data[0].content[0].text.value
    return jsonify({"reply": latest})

# For gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
