import os
import json
import redis
import uuid
import requests
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
ASSISTANT_ID = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load BlueJay brain
with open("bluejay/bluejay_config.json", "r") as f:
    bluejay_brain = json.load(f)

def get_thread_id(session_id):
    key = f"thread:{session_id}"
    thread_id = r.get(key)
    if thread_id:
        return thread_id.decode()
    new_thread = client.beta.threads.create()
    r.set(key, new_thread.id)
    return new_thread.id

def extract_conversation_info(message):
    info = {}
    lowered = message.lower()
    if "volume" in lowered or "$" in lowered:
        for word in lowered.split():
            if "$" in word or "k" in word:
                info["monthly_volume"] = word
    if "ticket" in lowered:
        for word in lowered.split():
            if word.replace(".", "", 1).isdigit():
                info["average_ticket"] = word
    if "square" in lowered or "stripe" in lowered:
        info["processor"] = "Square" if "square" in lowered else "Stripe"
    if any(x in lowered for x in ["mobile", "truck", "on the go"]):
        info["setup"] = "mobile"
    if "not interested" in lowered or "too expensive" in lowered:
        info["objection"] = "cost"
    if "ready" in lowered or "move forward" in lowered:
        info["urgency"] = "high"
    return info

def submit_to_hubspot(contact, note):
    token = os.getenv("HUBSPOT_TOKEN")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "properties": {
            "firstname": contact["name"],
            "phone": contact["phone"],
            "email": contact["email"],
            "bluejay_notes": note
        }
    }
    res = requests.post("https://api.hubapi.com/crm/v3/objects/contacts", headers=headers, json=data)
    return res.text if res.ok else f"Error: {res.text}"

@app.route("/", methods=["GET"])
def index():
    return """
    <html>
      <head><title>BlueJay Backend</title></head>
      <body style="background-color:#000; color:#fff; font-family:sans-serif; text-align:center; padding:50px;">
        <h1>BlueJay backend is live</h1>
      </body>
    </html>
    """

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = request.remote_addr
    message = data.get("message", "")
    thread_id = get_thread_id(session_id)

    r.rpush(f"log:{session_id}", message)
    memory_key = f"mem:{session_id}"
    memory = json.loads(r.get(memory_key) or "{}")

    extracted = extract_conversation_info(message)
    memory.update(extracted)

    capture_keys = ["name", "phone", "email"]
    for item in bluejay_brain.get("capture_sequence", []):
        key = item["key"]
        if key not in memory:
            memory[key] = message
            r.set(memory_key, json.dumps(memory))
            return jsonify({"reply": item["prompt"].replace("{name}", memory.get("name", ""))})

    if all(k in memory for k in capture_keys):
        if not memory.get("submitted"):
            note = f"Conversation Notes:\n"
            for k, v in memory.items():
                if k not in capture_keys and k != "submitted":
                    note += f"• {k.replace('_', ' ').title()}: {v}\n"
            result = submit_to_hubspot(
                {"name": memory["name"], "phone": memory["phone"], "email": memory["email"]},
                note
            )
            memory["submitted"] = True
            r.set(memory_key, json.dumps(memory))
            return jsonify({"reply": bluejay_brain["hubspot_trigger"]["submit_message"].replace("{name}", memory["name"])})

    r.set(memory_key, json.dumps(memory))
    return jsonify({"reply": "Got it — want to keep going or see your savings next?"})
