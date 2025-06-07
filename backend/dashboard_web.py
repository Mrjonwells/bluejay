import os
import redis
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="BlueJay Admin Console", layout="wide")
st.markdown("<h1 style='color:#00aaff;'>📊 BlueJay Admin Console</h1>", unsafe_allow_html=True)
st.markdown("---")

# Redis connection
redis_status = "Unknown"
redis_url = os.getenv("REDIS_URL")

try:
    pool = redis.ConnectionPool.from_url(redis_url, decode_components=True, ssl=False)
    redis_client = redis.Redis(connection_pool=pool)
    redis_client.ping()
    redis_status = "Connected"
except Exception as e:
    redis_status = f"Redis Connection Failed: {e}"
    st.error(redis_status)
    st.exception(e)

if "Connected" in redis_status:
    st.success("✅ Redis Connected")

# Usage Metrics
from dashboard import get_all_metrics
data = get_all_metrics()

st.markdown("## 💰 Current Spend Overview")
st.bar_chart({
    "GitHub": [data["GitHub"]["cost"]],
    "OpenAI": [data["OpenAI"]["cost"]],
    "Render": [data["Render"]["cost"]],
    "Total": [data["Total"]["cost"]]
})

st.markdown("## 📈 Usage Limits")
st.write(f"**OpenAI:** {data['OpenAI']['cost']} / {data['OpenAI']['limit']}")
st.write(f"**Render:** {data['Render']['cost']} / {data['Render']['limit']}")
st.write(f"**GitHub Actions:** {data['GitHub']['cost']} / {data['GitHub']['limit']}")
st.write(f"**Total Usage:** {data['Total']['cost']} / {data['Total']['limit']}")

st.markdown("---")
st.caption("BlueJay AI Admin Console © 2025")
