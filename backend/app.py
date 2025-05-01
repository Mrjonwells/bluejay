import os
import re
import uuid
import redis
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://askbluejay.ai"}})

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

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

    # Redis thread ID tracking
    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print(f"Redis get error: {e}")

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
        # Send user message
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Run assistant
        run_response = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Poll until complete
        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_response.id
            )
            if status.status == "completed":
                break

        # Get latest assistant message
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()

        # Detect submission trigger
        if re.search(r"\b(submit|done|that's all)\b", user_input.lower()):
            try:
                full_thread = "\n".join(
                    m.content[0].text.value for m in messages.data[:5]
                )
                name_match = re.search(r"(?i)name[:\s]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", full_thread)
                email_match = re.search(r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}", full_thread)
                phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", full_thread)
                company_match = re.search(r"(?i)business name[:\s]*(.+)", full_thread)

                fields = []
                if name_match:
                    fields.append({"name": "firstname", "value": name_match.group(1).split()[0]})
                    if len(name_match.group(1).split()) > 1:
                        fields.append({"name": "lastname", "value": name_match.group(1).split()[1]})
                if email_match:
                    fields.append({"name": "email", "value": email_match.group(0)})
                if phone_match:
                    fields.append({"name": "phone", "value": phone_match.group(0)})
                if company_match:
                    fields.append({"name": "company", "value": company_match.group(1).strip()})

                if fields:
                    hubspot_response = requests.post(
                        HUBSPOT_ENDPOINT,
                        headers={"Content-Type": "application/json"},
                        json={"fields": fields}
                    )
                    print("HubSpot submission response:", hubspot_response.status_code, hubspot_response.text)
            except Exception as e:
                print("HubSpot error:", e)

    except Exception as e:
        print(f"OpenAI API Error: {e}")
        assistant_reply = "Sorry, something went wrong connecting to the Assistant."

    return jsonify({'reply': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
