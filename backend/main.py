import os
import re
import uuid
import redis
import json
import random
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from openai import OpenAI

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://askbluejay.ai"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("message", "").strip()
    user_id = data.get("user_id", str(uuid.uuid4()))

    if not user_input:
        return {"reply": "Can you repeat that?"}

    thread_id = None
    if r:
        try:
            thread_id = r.get(f"thread:{user_id}")
            if thread_id:
                thread_id = thread_id.decode()
        except:
            pass

    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        if r:
            r.set(f"thread:{user_id}", thread_id)

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_input
    )

    run_response = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        stream=True
    )

    def stream_response():
        try:
            for chunk in client.beta.threads.runs.stream(
                thread_id=thread_id,
                run_id=run_response.id
            ):
                if chunk.status == "completed":
                    break
                yield json.dumps({"partial": chunk.status}) + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")
