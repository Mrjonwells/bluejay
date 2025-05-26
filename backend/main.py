import os
import json
import redis
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from waitress import serve
from datetime import datetime
import random

from backend.blog_engine import get_trending_topic, generate_blog_content

# Load environment
load_dotenv()

app = Flask(__name__)
CORS(app)

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config", "bluejay_config.json")
template_path = os.path.join(base_dir, "config", "conversation_template.json")
objection_log_path = os.path.join(base_dir, "backend", "logs", "objection_log.jsonl")

# Load brain and template
with open(config_path, "r") as f:
    brain = json.load(f)
try:
    with open(template_path, "r") as tf:
        template = json.load(tf)
except:
    template = {}

# Redis
redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url)

# OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
assistant_id = os.getenv("OPENAI_ASSISTANT_ID", "asst_bLMfZI9fO9E5jltHY8KDq9ZT")

# HubSpot
HUBSPOT_FORM_URL = "https://api.hsforms.com/submissions/v3/integration/submit/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"

# Objection keywords
OBJECTION_KEYWORDS = [
    "not interested", "already have", "too expensive", "let me think", "maybe later", "busy right now"
]

def redis_key(thread_id): return f"thread:{thread_id}"

def extract_fields(messages):
    name = phone = email = None
    for msg in messages:
        if msg["role"] != "user":
            continue
        content = msg["content"]
        if not name and any(w in content.lower() for w in ["i'm", "my name is", "this is"]) and len(content.split()) <= 6:
            name = content
        if not phone and any(char.isdigit() for char in content) and len(content) >= 10:
            digits = ''.join(filter(str.isdigit, content))
            if len(digits) >= 10:
                phone = digits
        if not email and "@" in content and "." in content:
            email = content
    return name, phone, email

def send_to_hubspot(name, phone, email, notes):
    payload = {
        "fields": [
            {"name": "firstname", "value": name},
            {"name": "phone", "value": phone},
            {"name": "email", "value": email},
            {"name": "notes", "value": notes}
        ],
        "context": {
            "pageUri": "https://askbluejay.ai",
            "pageName": "AskBlueJay.ai"
        },
        "legalConsentOptions": {
            "consent": {
                "consentToProcess": True,
                "text": "I agree to allow AskBlueJay.ai to store and process my personal data.",
                "communications": [{"value": True, "subscriptionTypeId": 999, "text": "I agree to receive marketing communications"}]
            }
        }
    }
    requests.post(HUBSPOT_FORM_URL, json=payload)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    thread_id = data.get("thread_id", "default")
    memory_key = redis_key(thread_id)

    if user_input.strip().lower() == "end chat":
        redis_client.delete(memory_key)
        redis_client.delete(f"{memory_key}:submitted")
        return jsonify({"reply": "Thanks for chatting with BlueJay. Your session is now closed."})

    history = redis_client.get(memory_key)
    thread_messages = json.loads(history) if history else []

    if not thread_messages:
        reply = "Hi, I’m BlueJay, your merchant AI expert. What’s your name?"
        thread_messages.append({"role": "assistant", "content": reply})
        redis_client.setex(memory_key, 1800, json.dumps(thread_messages))
        return jsonify({"reply": reply})
    elif len(thread_messages) == 1 and thread_messages[0]["role"] == "assistant" and "welcome back" not in thread_messages[0]["content"].lower():
        reply = "Welcome back — ready to pick up where we left off?"
        thread_messages.append({"role": "assistant", "content": reply})
        redis_client.setex(memory_key, 1800, json.dumps(thread_messages))
        return jsonify({"reply": reply})

    thread_messages.append({"role": "user", "content": user_input})

    if any(keyword in user_input.lower() for keyword in OBJECTION_KEYWORDS):
        try:
            with open(objection_log_path, "a") as f:
                f.write(json.dumps({"thread_id": thread_id, "messages": thread_messages}) + "\n")
        except Exception as e:
            print(f"Objection log error: {e}")

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

        name, phone, email = extract_fields(thread_messages)
        if name and phone and email and not redis_client.get(f"{memory_key}:submitted"):
            notes = "\n".join([f"{m['role']}: {m['content']}" for m in thread_messages])
            send_to_hubspot(name, phone, email, notes)
            redis_client.set(f"{memory_key}:submitted", "yes", ex=3600)

        return jsonify({"reply": reply})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

@app.route("/seo/trending", methods=["GET"])
def api_trending():
    return jsonify({"rewritten_topic": get_trending_topic()})

@app.route("/seo/inject", methods=["POST"])
def api_inject():
    data = request.get_json()
    topic = data.get("topic", "AI Trends")
    result = generate_blog_content(topic)
    return jsonify(result)

@app.route("/")
def home():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
