import streamlit as st
import redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="BlueJay Dashboard", layout="wide")

st.title("BlueJay Live Dashboard")

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
try:
    redis_client = redis.from_url(redis_url)
    keys = redis_client.keys("thread:*")
    st.success(f"Redis Connected — {len(keys)} active chat threads")
except Exception as e:
    st.error(f"Redis Connection Failed: {e}")
    keys = []

high = medium = low = 0
leads = []

for key in keys:
    try:
        data = redis_client.get(key)
        if not data: continue
        payload = json.loads(data)
        messages = payload.get("messages", [])
        for msg in messages:
            if msg["role"] == "assistant" and "lead_quality" in msg["content"].lower():
                if "high" in msg["content"].lower(): high += 1
                elif "medium" in msg["content"].lower(): medium += 1
                elif "low" in msg["content"].lower(): low += 1
        leads.append((key, len(messages)))
    except:
        continue

col1, col2, col3 = st.columns(3)
col1.metric("High Quality Leads", high)
col2.metric("Medium Quality Leads", medium)
col3.metric("Low Quality Leads", low)

st.subheader("Active Sessions")
for thread_id, msg_count in leads:
    st.write(f"{thread_id} — {msg_count} messages")
