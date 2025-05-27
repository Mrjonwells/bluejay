import streamlit as st
import os
from dotenv import load_dotenv
import redis
import pandas as pd
import time

load_dotenv()

# Secure login credentials
USERNAME = os.getenv("DASHBOARD_USER", "admin")
PASSWORD = os.getenv("DASHBOARD_PASS", "bluejay123")

# Simulated Redis connection
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# --- AUTHENTICATION ---
def login():
    st.title("🔐 BlueJay Dashboard Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == USERNAME and pw == PASSWORD:
            st.session_state.logged_in = True
        else:
            st.error("Invalid credentials")

# --- DASHBOARD CONTENT ---
def dashboard():
    st.set_page_config(page_title="BlueJay Admin Dashboard", layout="wide")
    st.title("📊 BlueJay AI Admin Dashboard")
    st.markdown("Real-time system stats, engagement metrics, and lead quality visualization.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Sessions", r.dbsize())
    with col2:
        st.metric("System Uptime", f"{round(time.time() - float(r.get('boot_time') or time.time()))}s")
    with col3:
        st.metric("Known Leads", len(r.keys("lead:*")))

    st.subheader("💡 Engagement Summary")
    lead_scores = []
    for key in r.scan_iter("lead:*"):
        data = r.hgetall(key)
        if 'score' in data:
            lead_scores.append(int(data['score']))

    if lead_scores:
        df = pd.DataFrame(lead_scores, columns=["Score"])
        st.bar_chart(df)
    else:
        st.info("No lead scores found.")

# --- ROUTER ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    dashboard()
else:
    login()
