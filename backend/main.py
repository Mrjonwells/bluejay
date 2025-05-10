import os
import json
import redis
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config paths
CONFIG_PATH = "backend/config/bluejay_config.json"
TEMPLATE_PATH = "backend/config/conversation_template.json"
LOG_PATH = "backend/logs/interaction_log.jsonl"

# Initialize app and services
app = Flask(__name__)
CORS(app)
client = OpenAI()
r = redis.from_url(os.getenv("REDIS_URL"))

# Load BlueJay config ("brain") and sales template
with open(CONFIG_PATH, "r") as f:
    BLUEJAY_CONFIG = json.load(f)
with open(TEMPLATE_PATH, "r") as f:
    CONVERSATION_TEMPLATE = json.load(f)

ASSISTANT_ID = os.getenv("OPENAI_ASSISTANT_ID")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    thread_id = data.get("thread_id")
    user_input = data.get("message", "")

    if not thread_id or not user_input:
        return jsonify({"error": "Missing thread_id or message"}), 400

    # Store user input in Redis
    r.rpush(thread_id, json.dumps({"user": user_input}))

    # Build context from memory
    history = [json.loads(r.lindex(thread_id, i)) for i in range(r.llen(thread_id)) if r.lindex(thread_id, i)]
    messages = [{"role": "user", "content": item["user"]} if "user" in item else item for item in history]

    # Inject config into system prompt
    system_prompt = {
        "role": "system",
        "content": f"You are BlueJay, a smart AI assistant using this config: {json.dumps(BLUEJAY_CONFIG)} and sales flow: {json.dumps(CONVERSATION_TEMPLATE)}"
    }
    messages.insert(0, system_prompt)

    # Chat completion
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5
    )

    reply = response.choices[0].message.content
    r.rpush(thread_id, json.dumps({"assistant": reply}))

    # Log the interaction
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as log_file:
        log_file.write(json.dumps({"thread": thread_id, "user": user_input, "assistant": reply}) + "\n")

    return jsonify({"reply": reply})

@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
