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
import time

from blog_engine import get_trending_topic, generate_blog_content
from language_detection import is_non_english
from intent_detection import detect_intent
from rate_analysis import parse_rate_request, get_suggested_rate, estimate_savings
from prompt_optimizer import build_optimized_prompt
from lead_scoring import parse_lead_details, score_lead

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

redis_url = os.getenv("REDIS_URL")
redis_client = redis.from_url(redis_url)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HUBSPOT_FORM_URL = "https://api.hsforms.com/submissions/v3/integration/submit/45853776/3b7c289f-566e-4403-ac4b-5e2387c3c5d1"

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

def send_to_hubspot(name, phone, email, notes, lead_score=None):
    properties = [
        {"name": "firstname", "value": name},
        {"name": "phone", "value": phone},
        {"name": "email", "value": email},
        {"name": "notes", "value": notes}
    ]
    if lead_score is not None:
        label = "High" if lead_score >= 70 else "Medium" if lead_score >= 40 else "Low"
        properties.append({"name": "lead_quality", "value": label})
    payload = {
        "fields": properties,
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

def store_session(memory_key, thread_messages, name=None, lead_score=None):
    TTL = 1800  # default
    if lead_score is not None and lead_score >= 70:
        TTL = 86400  # high-quality: 24hr
    payload = {
        "timestamp": time.time(),
        "messages": thread_messages,
        "name": name
    }
    redis_client.setex(memory_key, TTL, json.dumps(payload))

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    thread_id = data.get("thread_id", "default")
    memory_key = redis_key(thread_id)

    if user_input.lower() == "end chat":
        redis_client.delete(memory_key)
        redis_client.delete(f"{memory_key}:submitted")
        return jsonify({"reply": "Thanks for chatting with BlueJay. Your session is now closed."})

    history_blob = redis_client.get(memory_key)
    try:
        memory_data = json.loads(history_blob) if history_blob else None
        if memory_data:
            if time.time() - memory_data.get("timestamp", 0) > 1800:
                redis_client.delete(memory_key)
                memory_data = None
    except Exception as e:
        print("Session decode error:", e)
        redis_client.delete(memory_key)
        memory_data = None

    thread_messages = memory_data.get("messages") if memory_data else []
    known_name = memory_data.get("name") if memory_data else None

    current_hour = datetime.now().hour
    time_greeting = (
        "Good morning" if current_hour < 12 else
        "Good afternoon" if current_hour < 18 else
        "Good evening"
    )

    if not thread_messages:
        reply = (
            f"{time_greeting}! I’m BlueJay — your AI-powered merchant expert.\n"
            "I help businesses cut fees, boost profits, and scale smarter.\n"
            "Let’s get started — what’s your name?"
        )
        store_session(memory_key, [{"role": "assistant", "content": reply}], name=None)
        return jsonify({"reply": reply})

    elif len(thread_messages) == 1 and thread_messages[0]["role"] == "assistant":
        reply = (
            f"{time_greeting}, {known_name}! Ready to pick up where we left off?"
            if known_name else
            f"{time_greeting}, welcome back — ready to pick up where we left off?"
        )
        thread_messages.append({"role": "assistant", "content": reply})
        store_session(memory_key, thread_messages, name=known_name)
        return jsonify({"reply": reply})

    thread_messages.append({"role": "user", "content": user_input})

    if any(keyword in user_input.lower() for keyword in OBJECTION_KEYWORDS):
        try:
            with open(objection_log_path, "a") as f:
                f.write(json.dumps({"thread_id": thread_id, "messages": thread_messages}) + "\n")
        except Exception as e:
            print("Objection log error:", e)

    lang_code = is_non_english(user_input)
    if lang_code:
        thread_messages.append({"role": "assistant", "content": f"Puedo ayudarte en {lang_code.upper()} también. ¿Quieres continuar en ese idioma?"})

    intent = detect_intent(user_input)
    savings_message = None
    if intent in ["savings_calc", "pricing_info"]:
        rate_info = parse_rate_request(user_input)
        if rate_info["rate"]:
            savings = estimate_savings(rate_info["rate"])
            savings_message = f"If you're paying {rate_info['rate']}%, we could save you about ${savings}/mo on $10k volume."
        elif rate_info["platform"]:
            default_rate = get_suggested_rate(rate_info["platform"])
            if default_rate:
                savings = estimate_savings(default_rate)
                savings_message = (
                    f"Most {rate_info['platform'].capitalize()} merchants pay around {default_rate}%.\n"
                    f"That means you could save about ${savings}/mo with BlueJay on $10k volume.\n"
                    "Would you like a full breakdown?"
                )

    system_prompt = {
        "role": "system",
        "content": build_optimized_prompt(brain, template)
    }
    messages = [system_prompt] + thread_messages
    if savings_message:
        messages.append({"role": "assistant", "content": savings_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        thread_messages.append({"role": "assistant", "content": reply})

        name, phone, email = extract_fields(thread_messages)
        stored_name = known_name or name
        lead_data = parse_lead_details(user_input)
        lead_score = score_lead(lead_data["volume"], lead_data["transactions"])

        store_session(memory_key, thread_messages, name=stored_name, lead_score=lead_score)

        if name and phone and email and not redis_client.get(f"{memory_key}:submitted"):
            notes = "\n".join([f"{m['role']}: {m['content']}" for m in thread_messages])
            send_to_hubspot(name, phone, email, notes, lead_score=lead_score)
            redis_client.set(f"{memory_key}:submitted", "yes", ex=3600)

        return jsonify({"reply": reply})
    except Exception as e:
        print("Chat error:", e)
        return jsonify({"reply": "Something went wrong."}), 500

@app.route("/seo/trending", methods=["GET"])
def trending():
    return jsonify(get_trending_topic())

@app.route("/seo/inject", methods=["POST"])
def inject():
    data = request.get_json()
    return jsonify(generate_blog_content(data))

@app.route("/")
def home():
    return "BlueJay backend is live."

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
