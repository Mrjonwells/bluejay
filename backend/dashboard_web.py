import os
import redis
import streamlit as st
import urllib.parse
from dotenv import load_dotenv
from brainstem import get_all_metrics  # unified interface

load_dotenv()

st.set_page_config(page_title="BlueJay Admin Console", layout="wide")
st.markdown("<h1 style='color:#00aaff;'>📊 BlueJay Admin Console</h1>", unsafe_allow_html=True)
st.markdown("---")

# Redis connection with SSL-aware scheme
redis_status = "Unknown"
redis_url = os.getenv("REDIS_URL")

try:
    parsed_url = urllib.parse.urlparse(redis_url)
    use_ssl = parsed_url.scheme == "rediss"
    redis_client = redis.from_url(redis_url, ssl=use_ssl)
    redis_client.ping()
    redis_status = "Connected"
except Exception as e:
    redis_status = f"Redis Connection Failed: {e}"
    st.error(redis_status)
    st.stop()

st.success("✅ Redis Connected")
st.markdown("### 🔎 BlueJay System Status")

# Metrics section
try:
    metrics = get_all_metrics()

    spend_labels = list(metrics.keys())
    spend_values = [metrics[k]["cost"] for k in spend_labels]
    spend_limits = [metrics[k]["limit"] for k in spend_labels]

    st.subheader("💰 Current Spend Overview")
    st.bar_chart(data=spend_values, use_container_width=True)

    st.subheader("📉 Usage Limits")
    for key in metrics:
        st.markdown(f"**{key}**: ${metrics[key]['cost']} of ${metrics[key]['limit']}")

except Exception as e:
    st.error(f"Metric load failed: {e}")

st.markdown("---")
st.caption("BlueJay AI Admin Console © 2025")
