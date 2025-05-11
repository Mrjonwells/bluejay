import os
import json
import openai
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
import requests
from datetime import datetime

# Load environment
load_dotenv()

# Constants and paths
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")
SEO_PATH = os.getenv("SEO_FILE_PATH", "backend/seo/seo_config.json")
HUBSPOT_FORM_ID = os.getenv("HUBSPOT_FORM_ID")
HUBSPOT_PORTAL_ID = os.getenv("HUBSPOT_PORTAL_ID")

# Load brain config
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

# Redis key generator
def redis_key(thread_id): return f"thread:{thread_id}"

# Auto-submit to HubSpot
def submit_to_hubspot(data):
    url = f"https://api.hsforms.com/submissions/v3/integration/submit/{HUBSPOT_PORTAL_ID}/{HUBSPOT_FORM_ID}"
    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print("HubSpot error:", e)

# Summarize and submit lead
def check_and_submit(thread_id, messages):
    text = " ".join(m["content"] for m in messages if m["role"] == "user").lower()
    email = next((m["content"] for m in messages if "@" in m["content"]), None)
    phone = next((m["content"] for m in messages if "call" in m["content"] or "text" in m["content"]), None)
    name = next((m["content"] for m in messages if "name is" in m["content"] or "i'm" in m["content"]), None)

    if email and phone and name:
        summary = f"Name: {name}\nPhone: {phone}\nEmail: {email}\n\nConversation:\n" + \
                  "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        fields = [
            {"name": "firstname", "value": name},
            {"name": "email", "value": email},
            {"name": "phone", "value": phone}
        ]
        hs_data = {"fields": fields, "context": {"pageUri": "https://askbluejay.ai", "pageName": "BlueJay AI"},
                   "legalConsentOptions": {"consent": {"consentToProcess": True, "text": "I agree."}}}
        submit_to_hubspot(hs_data)
        redis_client.delete(redis_key(thread_id))

# Routes
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id") or str(uuid.uuid4())
    user_input = data["message"]

    # Load thread
    history = redis_client.get(redis_key(thread_id))
    messages = json.loads(history) if history else []
    messages.append({"role": "user", "content": user_input})

    # OpenAI assistant call
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template:\n{json.dumps(conversation_template)}"},
                *messages
            ],
            temperature=0.7
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "Something went wrong."
        print("OpenAI error:", e)

    messages.append({"role": "assistant", "content": reply})
    redis_client.setex(redis_key(thread_id), 1800, json.dumps(messages))
    check_and_submit(thread_id, messages)

    return jsonify({"reply": reply, "thread_id": thread_id})

@app.route("/")
def home():
    return "BlueJay backend is running."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
