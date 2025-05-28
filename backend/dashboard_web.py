import streamlit as st
import os
import redis
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("DASHBOARD_USER", "admin")
PASSWORD = os.getenv("DASHBOARD_PASS", "bluejay123")
REDIS_URL = os.getenv("REDIS_URL")

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
        st.code(f"Redis URL → {REDIS_URL}")
        r = redis.from_url(REDIS_URL, decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        st.error(f"❌ Redis Connection Failed: {e}")
        return None

def dashboard():
    st.title("🧠 BlueJay Admin Console")
    st.subheader("📊 BLUEJAY STATUS")

    r = connect_redis()
    if not r:
        return

    st.metric("Active Sessions", r.dbsize())
    st.success("✅ Redis connected")

if __name__ == "__main__":
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        login()
    else:
        dashboard()
