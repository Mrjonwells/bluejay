import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Redis setup
redis_url = os.getenv("REDIS_URL")
r = redis.Redis.from_url(redis_url) if redis_url else None

# Flask secret
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")

# OpenAI setup
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message', '')
    user_id = data.get('user_id', str(uuid.uuid4()))

    if not user_input:
        return jsonify({'response': "I didn't catch that. Try again."})

    # Redis thread ID (optional tracking)
    if r:
        thread_id = r.get(f"thread:{user_id}")
        if not thread_id:
            thread_id = f"thread_{str(uuid.uuid4())}"
            r.set(f"thread:{user_id}", thread_id)

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
        assistant_reply = "Sorry, something went wrong."

    return jsonify({'response': assistant_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
