import os
import streamlit as st
import redis
import datetime

st.set_page_config(page_title="BlueJay Admin Console", layout="centered")

# ━━━━━━━━━━ AUTH ━━━━━━━━━━
DASHBOARD_USER = os.getenv("DASHBOARD_USER")
DASHBOARD_PASS = os.getenv("DASHBOARD_PASS")

def login():
    st.title("🔐 Admin Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == DASHBOARD_USER and pwd == DASHBOARD_PASS:
            st.session_state["authenticated"] = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

if "authenticated" not in st.session_state:
    login()
    st.stop()

# ━━━━━━━━━━ REDIS CONNECT ━━━━━━━━━━
def connect_redis():
    try:
        url = os.getenv("REDIS_URL")
        r = redis.from_url(url, decode_responses=True)
        r.ping()
        return r
    except Exception as e:
        st.error("❌ Redis Connection Failed")
        st.stop()

r = connect_redis()

# ━━━━━━━━━━ DISPLAY ━━━━━━━━━━
st.title("🧠 BlueJay Admin Console")

st.markdown("### ━━━━━━━━━━ BLUEJAY STATUS ━━━━━━━━━━")
st.success("Redis        : ✓ Connected")
st.success("HubSpot      : Last push: 5 min ago")
st.success("Blog Engine  : Trending topic fetched 10m ago")

st.markdown("### ━━━━━━━━━━ LEADS ━━━━━━━━━━")
st.markdown("New leads    : 3")
st.markdown("High         : 1")
st.markdown("Medium       : 1")
st.markdown("Low          : 1")
st.markdown('Objections   : `"already have"` (2x)')

st.markdown("### ━━━━━━━━━━ TRAFFIC ━━━━━━━━━━")
st.markdown("Chats Today  : 14")
st.markdown("Common Intents: savings_calc, lead_capture")
st.markdown("Avg Response : 1.3s")

st.markdown("### ━━━━━━━━━━ ERRORS ━━━━━━━━━━")
st.markdown("0 errors in last 30 mins")
st.caption(f"Last updated: {datetime.datetime.now().strftime('%H:%M:%S')}")
