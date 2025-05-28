import os
import redis
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="BlueJay Admin Console", layout="wide")

st.markdown("<h1 style='color:#f63366;'>🧠 BlueJay Admin Console</h1>", unsafe_allow_html=True)
st.markdown("---")

redis_status = "Unknown"
redis_url = os.getenv("REDIS_URL")

try:
    redis_client = redis.Redis.from_url(redis_url, socket_connect_timeout=5)
    redis_client.ping()
    redis_status = "Connected"
except Exception as e:
    redis_status = f"Redis Connection Failed: {e}"
    st.exception(e)

if "Connected" in redis_status:
    st.success("✅ Redis Connected")
else:
    st.error(f"❌ {redis_status}")

st.markdown("### BLUEJAY STATUS")
st.markdown("*Coming soon: Lead scores, chat logs, and topic stats.*")
st.spinner("Loading components...")
st.markdown("---")
st.caption("BlueJay AI Admin Console © 2025")
