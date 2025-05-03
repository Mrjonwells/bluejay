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

config_path = os.path.join(os.path.dirname(__file__), "bluejay", "bluejay_config.json")
with open(config_path) as f:
    config = json.load(f)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"response": "Can you repeat that?"})

    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print("Redis error:", e)

    if not thread_id:
        try:
            thread = client.beta.threads.create()
            thread_id = thread.id
            if r:
                r.set(f"thread:{user_id}", thread_id)
        except Exception as e:
            print("Thread error:", e)
            return jsonify({"response": "I'm having trouble starting a new conversation."})

    try:
        client.beta.threads.messages.create(thread_id=thread_id, role="user", content=user_input)
        run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

        while True:
            status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        reply = messages.data[0].content[0].text.value.strip()

        # Shorten long replies
        if reply.count(".") > 2 or len(reply.split()) > 50:
            reply = reply.split(".")[0] + "..."

        text = user_input.lower()
        stage = "curious"
        for s, kws in config["deal_stage_scoring"].items():
            if any(k in text for k in kws):
                stage = s
                break
        tone_block = config["deal_stage_tone"].get(stage)
        if tone_block:
            reply += "\n\n" + tone_block["example"]

        if len(messages.data) < 3:
            reply = random.choice(config["forward_prompts"])

        for key, val in config["objections"].items():
            if key in text:
                reply += "\n\n" + val
                break

        if random.random() < 0.15:
            reply += "\n\n" + random.choice(config["urgency_triggers"])

        tone = "confident"
        if "?" in user_input:
            tone = "friendly"
        if any(x in text for x in ["later", "wait", "stall"]):
            tone = "urgency"
        if random.random() < 0.33:
            emoji = random.choice(config["emoji_logic"]["tones"].get(tone, []))
            reply += f" {emoji}"

        # Estimate savings
        monthly = rate = None
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
            annual = round(monthly * rate * 12 / 100)
            template = config["annual_savings_formula"]["response_template"]
            reply += "\n\n" + template.replace("{rate}", str(rate)).replace("{savings}", str(annual))

        # Recommend Clover
        for k, v in config["product_recommendations"].items():
            if any(kw in text for kw in v["keywords"]):
                reply += "\n\n" + v["reply"]
                break

        # Save history
        if r:
            try:
                r.rpush(f"log:{user_id}", user_input)
                r.expire(f"log:{user_id}", 3600)
            except Exception as e:
                print("Redis log error:", e)

    except Exception as e:
        print("Final handler error:", e)
        reply = "Oops. I ran into a technical issue."

    return jsonify({"response": reply})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))