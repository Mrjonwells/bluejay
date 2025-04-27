import os
import time
import redis
import requests
import re
import uuid
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis setup with fallback
redis_url = os.getenv("REDIS_URL")
r = None

if redis_url:
    try:
        r = redis.Redis.from_url(redis_url)
        r.ping()
        print("Connected to Redis successfully.")
    except Exception as e:
        print(f"Warning: Redis connection failed — running without Redis. Error: {e}")
        r = None
else:
    print("No Redis URL provided — running without Redis.")

# Flask secret
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Static folder serving (for frontend)
@app.route('/')
def serve_index():
    return send_from_directory('', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('', path)

# Main chat endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    user_id = data.get('user_id', str(uuid.uuid4()))

    if not user_input:
        return jsonify({'response': "I'm sorry, I didn't receive any input."})

    # Get or create a thread ID
    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except Exception as e:
            print(f"Redis get error: {e}")

    if not thread_id:
        thread_id = f"thread_{str(uuid.uuid4())}"
        if r:
            try:
                r.set(f"thread:{user_id}", thread_id)
            except Exception as e:
                print(f"Redis set error: {e}")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are BlueJay, a helpful merchant savings assistant."},
                {"role": "user", "content": user_input}
            ]
        )
        assistant_reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        assistant_reply = "Sorry, I'm having trouble responding right now."

    return jsonify({'response': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
