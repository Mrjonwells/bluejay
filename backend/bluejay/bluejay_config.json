import os
import re
import uuid
import redis
import json
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://askbluejay.ai"}})

# Redis
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load config
with open("bluejay/bluejay_config.json") as f:
    config = json.load(f)

# HubSpot info
HUBSPOT_PORTAL_ID = "45853776"
HUBSPOT_FORM_GUID = "3b7c289f-566e-4403-ac4b-5e2387c3c5d1"
HUBSPOT_ENDPOINT = f"https://api.hsforms.com/submissions/v3/integration/submit/{HUBSPOT_PORTAL_ID}/{HUBSPOT_FORM_GUID}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    user_id = data.get('user_id', str(uuid.uuid4()))

    if not user_input:
        return jsonify({'reply': "I didn't catch that. Try again."})

    # Detect personality type
    personality_type = "friendly"
    if any(word in user_input.lower() for word in ["data", "cost", "rate", "how much", "analyze"]):
        personality_type = "analytical"
    elif any(word in user_input.lower() for word in ["scam", "not sure", "seems shady"]):
        personality_type = "skeptical"
    elif any(word in user_input.lower() for word in ["hurry", "busy", "quick", "fast"]):
        personality_type = "rushed"
    style_hint = config["personality_modes"].get(personality_type, {}).get("response_style", "")
    print(f"Detected personality: {personality_type} | Style: {style_hint}")

    # Redis thread memory
    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print(f"Redis error: {e}")

    if not thread_id:
        try:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)
        except Exception as e:
            print(f"Thread creation error: {e}")
            return jsonify({'reply': "Sorry, I'm having trouble starting the conversation."})

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

        # Trigger fallback if contact fields are complete but user hesitates
        if config.get("fallback_closure", {}).get("trigger_after_contact_fields"):
            combined = "\n".join(m.content[0].text.value for m in messages.data[:6])
            if all(x in combined.lower() for x in ["name", "email", "phone", "business"]):
                if not any(p in user_input.lower() for p in config["trigger_phrases"]):
                    assistant_reply += f"\n\n{config['fallback_closure']['fallback_message']}"

        # Trigger HubSpot lead submission
        if any(phrase in user_input.lower() for phrase in config["trigger_phrases"]):
            try:
                thread_text = "\n".join(m.content[0].text.value for m in messages.data[:5])
                name = re.search(r"(?i)name[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", thread_text)
                email = re.search(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", thread_text)
                phone = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", thread_text)
                company = re.search(r"(?i)business name[:\s]*(.+)", thread_text)

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
                    res = requests.post(HUBSPOT_ENDPOINT,
                        headers={"Content-Type": "application/json"},
                        json={"fields": fields}
                    )
                    print("HubSpot response:", res.status_code, res.text)
            except Exception as e:
                print("HubSpot error:", e)

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        assistant_reply = "Sorry, something went wrong connecting to the Assistant."

    return jsonify({'reply': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
