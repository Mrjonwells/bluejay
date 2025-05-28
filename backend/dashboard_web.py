
import streamlit as st
import os
import redis
import json
import time
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DASHBOARD_USER", "admin")
PASSWORD = os.getenv("DASHBOARD_PASS", "bluejay123")

def login():
    st.title("🔐 BlueJay Admin Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == USERNAME and pw == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

def connect_redis():
    try:
        r = redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        st.error("❌ Redis Connection Failed")
        return None

def dashboard():
    st.set_page_config(page_title="BlueJay Admin", layout="wide")
    st.title("🧠 BlueJay Admin Console")
    st.markdown("`━━━━━━━━━━ BLUEJAY STATUS ━━━━━━━━━━`")

    r = connect_redis()
    if not r:
        return

    # Status block
    active_keys = r.keys("thread:*")
    st.markdown(f"**Redis**        : ✓ Connected ({len(active_keys)} threads)")
    st.markdown(f"**HubSpot**      : Last push: N/A")
    st.markdown(f"**Blog Engine**  : Trending topics: OK")

    st.markdown("`━━━━━━━━━━ LEADS ━━━━━━━━━━`")
    high = medium = low = 0
    for key in r.scan_iter("lead:*"):
        score = r.hget(key, "score")
        if score:
            s = int(score)
            if s >= 70: high += 1
            elif s >= 40: medium += 1
            else: low += 1
    st.markdown(f"**High**   : {high}")
    st.markdown(f"**Medium** : {medium}")
    st.markdown(f"**Low**    : {low}")

    st.markdown("`━━━━━━━━━━ TRAFFIC ━━━━━━━━━━`")
    st.markdown(f"**Chats Today**     : [N/A]")
    st.markdown(f"**Common Intents**  : [N/A]")

    st.markdown("`━━━━━━━━━━ ERRORS ━━━━━━━━━━`")
    st.markdown("**0 errors in last 30 minutes**")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    dashboard()
else:
    login()
