import os
import redis
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app, origins=["https://rococo-gecko-93903b.netlify.app"])  # <-- CORS fixed here

# Environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("ASSISTANT_ID")
redis_url = os.getenv("REDIS_URL")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")

# Setup Redis
r = redis.from_url(redis_url)

# Setup OpenAI client
client = OpenAI(api_key=openai_api_key)

# Flask secret
app.secret_key = flask_secret_key or "supersecret"