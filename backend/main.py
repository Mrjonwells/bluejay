import os
import time
import redis
import openai
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Config paths
CONFIG_PATH = "backend/config/bluejay_config.json"
CONVO_TEMPLATE_PATH = "backend/config/conversation_template.json"

# Load assistant + config brain
with open(CONFIG_PATH, "r") as f:
    brain_config = json.load(f)
with open(CONVO_TEMPLATE_PATH, "r") as f:
    convo_template = json.load(f)

# Init app
app = Flask(__name__)
CORS(app)
openai.api_key = os.getenv("OPENAI_API_KEY")
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url)

# Assistant identity
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Thread TTL (30 min)
TTL = 1800

def log_interaction(user_msg, assistant_msg, thread_id):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "thread_id": thread_id,
        "user": user_msg,
        "assistant": assistant_msg
    }
    with open("backend/logs/interaction_log.jsonl", "a") as f:
        f.write(json.dumps(log) + "\n")
    print("Logged interaction")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()
    thread_id = data.get("thread_id") or f"thread_{int(time.time()*1000)}"

    if not user_input:
        return jsonify({"error": "Empty message"}), 400

    # Recall or create thread
    redis_key = f"thread:{thread_id}"
    if not r.exists(redis_key):
        r.set(redis_key, json.dumps([]), ex=TTL)
    else:
        r.expire(redis_key, TTL)

    # Update memory
    history = json.loads(r.get(redis_key))
    history.append({"role": "user", "content": user_input})
    r.set(redis_key, json.dumps(history), ex=TTL)

    # Send to assistant
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are BlueJay, a smart assistant that helps close merchant processing deals."},
                {"role": "system", "content": json.dumps(brain_config)},
                {"role": "system", "content": json.dumps(convo_template)},
                *history
            ],
            max_tokens=400,
            temperature=0.7
        )
        reply = response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Update thread + log
    history.append({"role": "assistant", "content": reply})
    r.set(redis_key, json.dumps(history), ex=TTL)
    log_interaction(user_input, reply, thread_id)

    return jsonify({"response": reply, "thread_id": thread_id})

if __name__ == "__main__":
    app.run(debug=True)
