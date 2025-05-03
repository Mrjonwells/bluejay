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

# Load config from subdirectory
config_path = os.path.join(os.path.dirname(__file__), "bluejay", "bluejay_config.json")
with open(config_path) as f:
    config = json.load(f)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return jsonify({"reply": "Can you repeat that?"})

    print("USER INPUT:", user_input)
    print("USER ID:", user_id)

    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
            print("Redis thread ID:", thread_id)
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
            print("Created new thread:", thread_id)
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
        print("Run created:", run_response.id)

        while True:
            status = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_response.id
            )
            print("Run status:", status.status)
            if status.status == "completed":
                break

        messages = client.beta.threads.messages.list(thread_id=thread_id)
        assistant_reply = messages.data[0].content[0].text.value.strip()
        print("Raw assistant reply:", assistant_reply)

        # Truncate long replies
        if assistant_reply.count(".") > 2 or len(assistant_reply.split()) > 50:
            assistant_reply = assistant_reply.split(".")[0] + "..."

        user_text_lower = user_input.lower()

        # Score deal stage
        current_stage = "curious"
        for stage, keywords in config.get("deal_stage_scoring", {}).items():
            if any(kw in user_text_lower for kw in keywords):
                current_stage = stage
                break
        tone_block = config["deal_stage_tone"].get(current_stage)
        if tone_block:
            assistant_reply += "\n\n" + tone_block["example"]

        if len(messages.data) < 3:
            assistant_reply = random.choice(config["forward_prompts"])

        for key, rebuttal in config["objections"].items():
            if key in user_text_lower:
                assistant_reply += "\n\n" + rebuttal
                break

        if random.random() < 0.15:
            assistant_reply += "\n\n" + random.choice(config["urgency_triggers"])

        tone = "confident"
        if "?" in user_input:
            tone = "friendly"
        if any(x in user_text_lower for x in ["later", "wait", "stall"]):
            tone = "urgency"
        if random.random() < 0.33:
            emoji = random.choice(config["emoji_logic"]["tones"].get(tone, []))
            assistant_reply += f" {emoji}"

        # Annual savings estimate
        monthly = None
        rate = None
        for m in reversed(messages.data):
            text = m.content[0].text.value.lower()
            if "volume" in text or "$" in text:
                match = re.search(r"\$?(\d+[,.]?\d+)", text)
                if match:
                    monthly = float(match.group(1).replace(",", ""))
            if "%" in text:
                match = re.search(r"(\d+(\.\d+)?)%", text)
                if match:
                    rate = float(match.group(1))
            if monthly and rate:
                break
        if monthly and rate:
            annual = round(monthly * rate * 12 / 100)
            line = config["annual_savings_formula"]["response_template"]
            assistant_reply += "\n\n" + line.replace("{rate}", str(rate)).replace("{savings}", str(annual))

        # Clover recommendation
        for product_key, product in config.get("product_recommendations", {}).items():
            if any(k in user_text_lower for k in product["keywords"]):
                assistant_reply += "\n\n" + product["reply"]
                break

        print("Final assistant reply:", assistant_reply)

    except Exception as e:
        print("OpenAI API error:", e)
        assistant_reply = "Something went wrong connecting to the assistant."

    return jsonify({"reply": assistant_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
