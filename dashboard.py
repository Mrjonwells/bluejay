# dashboard.py

import streamlit as st
import redis
import json
import os
from collections import Counter
import time
from datetime import datetime

st.set_page_config(page_title="BlueJay Admin Dashboard", layout="wide")

# Redis connection
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.from_url(redis_url)

# Title
st.title("BlueJay Intelligence Dashboard")

# Sidebar status
st.sidebar.header("System Health")
try:
    test_ping = r.ping()
    st.sidebar.success("Redis: Online")
except:
    st.sidebar.error("Redis: Offline")

# Load sessions
st.header("Recent Sessions")
keys = [k.decode() for k in r.keys("thread:*") if b":submitted" not in k]
sessions = []
for key in keys[-10:]:
    raw = r.get(key)
    if raw:
        data = json.loads(raw)
        sessions.append({
            "Thread": key,
            "Name": data.get("name", "—"),
            "Messages": len(data.get("messages", [])),
            "Last Seen": datetime.fromtimestamp(data.get("timestamp", 0)).strftime("%Y-%m-%d %H:%M"),
        })

if sessions:
    st.table(sessions)
else:
    st.info("No active sessions.")

# Lead Quality
st.header("Lead Quality Overview")
quality_counts = Counter()
for key in r.scan_iter("thread:*"):
    if b":submitted" not in key:
        data = r.get(key)
        if data:
            try:
                payload = json.loads(data)
                name = payload.get("name")
                if name:
                    score_key = key.decode().replace("thread:", "thread:") + ":submitted"
                    if r.get(score_key):
                        notes = "\n".join(m["content"] for m in payload.get("messages", []) if m["role"] == "user")
                        if "high" in notes.lower():
                            quality_counts["High"] += 1
                        elif "medium" in notes.lower():
                            quality_counts["Medium"] += 1
                        elif "low" in notes.lower():
                            quality_counts["Low"] += 1
            except:
                continue

st.bar_chart(quality_counts)

# Footer
st.markdown("Last updated: " + time.strftime("%Y-%m-%d %H:%M:%S"))
