import os
import re
import uuid
import redis
import json
import random
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://askbluejay.ai"}})

redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

with open("bluejay/bluejay_config.json") as f:
    config = json.load(f)

HUBSPOT_PORTAL_ID = "45853776"
HUBSPOT_FORM_GUID = "3b7c289f-566e-4403-ac4b-5e2387c3c5d1"
HUBSPOT_ENDPOINT = f"https://api.hsforms.com/submissions/v3/integration/submit/{HUBSPOT_PORTAL_ID}/{HUBSPOT_FORM_GUID}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"reply": "Can you repeat that?"})

    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print("Redis error:", e)

    is_new_thread = False
    if not thread_id:
        try:
            thread = client.beta.threads.create()
            thread_id = thread.id
            is_new_thread = True
            if r:
                r.set(f"thread:{user_id}", thread_id)
        except Exception as e:
            print("Thread creation error:", e)
            return jsonify({"reply": "Having trouble starting a new conversation. Try again shortly."})

    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run_response = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_response.id
            )
            if status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()

        # Industry tone logic
        industry_clues = {
            "retail": ["store", "retail", "shop", "boutique"],
            "food truck": ["truck", "vendor", "mobile"],
            "salon": ["salon", "spa", "stylist", "hair"],
            "auto repair": ["auto", "garage", "mechanic"],
            "ecommerce": ["shopify", "website", "ecommerce", "online"]
        }
        user_text_lower = user_input.lower()
        for industry, keywords in industry_clues.items():
            if any(k in user_text_lower for k in keywords):
                tone_note = config["industry_tone_map"].get(industry, "")
                if tone_note:
                    assistant_reply += f"\n\n[Note: {tone_note}]"
                break

        # Adaptive closers
        if any(x in user_text_lower for x in ["not interested", "no thanks"]):
            assistant_reply += "\n\n" + config["adaptive_closers"]["low_interest"]
        elif any(x in user_text_lower for x in ["later", "maybe", "not now"]):
            assistant_reply += "\n\n" + config["adaptive_closers"]["stall"]
        elif any(x in user_text_lower for x in ["just info", "just looking", "overview"]):
            assistant_reply += "\n\n" + config["adaptive_closers"]["info_only"]

        # HubSpot auto submission
        recent_text = "\n".join(m.content[0].text.value.lower() for m in messages.data[:6])
        if all(x in recent_text for x in ["name", "email", "phone", "business"]):
            name = re.search(r"(?i)name[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", recent_text)
            email = re.search(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", recent_text)
            phone = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", recent_text)
            company = re.search(r"(?i)business name[:\s]*(.+)", recent_text)
            fields = []
            if name:
                parts = name.group(1).split()
                fields.append({"name": "firstname", "value": parts[0]})
                if len(parts) > 1:
                    fields.append({"name": "lastname", "value": parts[1]})
            if email:
                fields.append({"name": "email", "value": email.group(0)})
            if phone:
                fields.append({"name": "phone", "value": phone.group(0)})
            if company:
                fields.append({"name": "company", "value": company.group(1).strip()})
            if fields:
                res = requests.post(
                    HUBSPOT_ENDPOINT,
                    headers={"Content-Type": "application/json"},
                    json={"fields": fields}
                )
                print("HubSpot response:", res.status_code, res.text)

        # Smart intro message
        if is_new_thread and assistant_reply.lower().startswith(("hi", "hello")):
            assistant_reply = random.choice(config.get("smart_intro_messages", [assistant_reply]))

    except Exception as e:
        print("OpenAI API error:", e)
        assistant_reply = "Something went wrong connecting to the assistant."

    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
