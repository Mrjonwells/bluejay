import os
import json
import openai
import redis
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve

# Load environment
load_dotenv()

# Load config
base_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(base_dir, "config", "bluejay_config.json")
TEMPLATE_PATH = os.path.join(base_dir, "config", "conversation_template.json")

with open(CONFIG_PATH, "r") as f:
    brain = json.load(f)

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

# Thread key generator
def redis_key(thread_id): return f"thread:{thread_id}"

# Helper to send to HubSpot
def send_to_hubspot(name, phone, email, summary):
    portal_id = os.getenv("HUBSPOT_PORTAL_ID")
    form_id = os.getenv("HUBSPOT_FORM_ID")
    url = f"https://api.hsforms.com/submissions/v3/integration/submit/{portal_id}/{form_id}"

    data = {
        "fields": [
            {"name": "firstname", "value": name},
            {"name": "phone", "value": phone},
            {"name": "email", "value": email}
        ],
        "context": {
            "pageUri": "https://askbluejay.ai",
            "pageName": "BlueJay Assistant"
        },
        "legalConsentOptions": {
            "consent": {
                "consentToProcess": True,
                "text": "By submitting, you agree to receive communication from BlueJay."
            }
        }
    }

    if summary:
        data["fields"].append({"name": "message", "value": summary})

    try:
        requests.post(url, json=data)
        print("HubSpot lead submitted.")
    except Exception as e:
        print("HubSpot error:", e)

# Routes
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    thread_id = data.get("thread_id", "default")
    user_input = data["message"]

    # Load prior messages
    history = redis_client.get(redis_key(thread_id))
    thread_messages = json.loads(history) if history else []

    # Add user input
    thread_messages.append({"role": "user", "content": user_input})

    # OpenAI call
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": f"You are BlueJay, a persuasive sales assistant. Use this brain:\n{json.dumps(brain)}\nAlso use this template:\n{json.dumps(conversation_template)}"},
            *thread_messages
        ],
        temperature=0.7
    )

    reply = response.choices[0].message.content
    thread_messages.append({"role": "assistant", "content": reply})
    redis_client.setex(redis_key(thread_id), 3600, json.dumps(thread_messages))

    # HubSpot trigger condition
    input_combined = " ".join([m["content"].lower() for m in thread_messages if m["role"] == "user"])
    if "@gmail.com" in input_combined or "@yahoo.com" in input_combined or "@outlook.com" in input_combined:
        if any(x in input_combined for x in ["text", "call", "reach me", "number"]) and "my name is" in input_combined:
            name = next((m["content"] for m in thread_messages if "my name is" in m["content"].lower()), "")
            phone = next((m["content"] for m in thread_messages if "text" in m["content"].lower() or "call" in m["content"].lower()), "")
            email = next((m["content"] for m in thread_messages if "@" in m["content"]), "")
            summary = "\n".join([f"{m['role']}: {m['content']}" for m in thread_messages])
            send_to_hubspot(name, phone, email, summary)

    return jsonify({"reply": reply})

@app.route("/")
def ping():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
