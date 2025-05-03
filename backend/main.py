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

# Redis
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
assistant_id = "asst_bLMfZI9fO9E5jltHY8KDq9ZT"

# Load BlueJay brain
brain_path = os.path.join(os.path.dirname(__file__), "bluejay", "bluejay_config.json")
with open(brain_path) as f:
    config = json.load(f)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"response": "Can you repeat that?"})

    try:
        thread_id = None
        if r:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()

        if not thread_id:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)
                r.expire(f"thread:{user_id}", 1800)

        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = messages.data[0].content[0].text.value.strip()

        user_text_lower = user_input.lower()

        # Stage scoring
        stage = "curious"
        for s, keywords in config.get("deal_stage_scoring", {}).items():
            if any(kw in user_text_lower for kw in keywords):
                stage = s
                break

        tone = config["deal_stage_tone"].get(stage)
        if tone:
            reply += "\n\n" + tone["example"]

        if len(messages.data) < 3:
            reply = random.choice(config["forward_prompts"])

        for key, rebuttal in config.get("objections", {}).items():
            if key in user_text_lower:
                reply += "\n\n" + rebuttal
                break

        if random.random() < 0.15:
            reply += "\n\n" + random.choice(config["urgency_triggers"])

        mood = "confident"
        if "?" in user_input:
            mood = "friendly"
        if any(x in user_text_lower for x in ["later", "wait", "stall"]):
            mood = "urgency"
        if random.random() < 0.33:
            emoji = random.choice(config["emoji_logic"]["tones"].get(mood, []))
            reply += f" {emoji}"

        # Annual savings
        monthly = None
        rate = None
        for m in reversed(messages.data):
            t = m.content[0].text.value.lower()
            if "volume" in t or "$" in t:
                match = re.search(r"\$?(\d+[,.]?\d+)", t)
                if match:
                    monthly = float(match.group(1).replace(",", ""))
            if "%" in t:
                match = re.search(r"(\d+(\.\d+)?)%", t)
                if match:
                    rate = float(match.group(1))
            if monthly and rate:
                break
        if monthly and rate:
            savings = round(monthly * rate * 12 / 100)
            line = config["annual_savings_formula"]["response_template"]
            reply += "\n\n" + line.replace("{rate}", str(rate)).replace("{savings}", str(savings))

        for k, product in config.get("product_recommendations", {}).items():
            if any(word in user_text_lower for word in product["keywords"]):
                reply += "\n\n" + product["reply"]
                break

        # Log memory and HubSpot note
        if r:
            try:
                key = f"log:{user_id}"
                r.rpush(key, user_input)
                r.expire(key, 1800)
                log = [x.decode() for x in r.lrange(key, 0, -1)]
                if len(log) > 3:
                    note = {
                        "engagement": {"active": True, "type": "NOTE"},
                        "associations": {"contactIds": []},
                        "metadata": {"body": "BlueJay Chat History:\n" + "\n".join(log)}
                    }
                    requests.post(
                        "https://api.hubapi.com/engagements/v1/engagements",
                        headers={
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {os.getenv('HUBSPOT_API_KEY')}"
                        },
                        json=note
                    )
            except Exception as e:
                print("HubSpot note error:", e)

        return jsonify({"response": reply})

    except Exception as e:
        print("Chat error:", e)
        return jsonify({"response": "Something went wrong on my end. Try again soon."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
