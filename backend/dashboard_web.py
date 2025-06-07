import os
import redis
import streamlit as st
from dotenv import load_dotenv
from dashboard import get_all_metrics
from brainstem import get_brain_code, save_brain_code

load_dotenv()
st.set_page_config(page_title="BlueJay Admin Console", layout="wide")
st.markdown("<h1 style='color:#00aaff;'>📊 BlueJay Admin Console</h1>", unsafe_allow_html=True)
st.markdown("---")

# Redis connection with SSL
redis_status = "Unknown"
redis_url = os.getenv("REDIS_URL")
try:
    redis_client = redis.from_url(redis_url, ssl=True)
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

    st.subheader("💰 Current Spend Overview")
    st.bar_chart(data=spend_values, use_container_width=True)

    st.subheader("📉 Usage Limits")
    for key in metrics:
        st.markdown(f"**{key}**: ${metrics[key]['cost']} of ${metrics[key]['limit']}")
except Exception as e:
    st.error(f"Metric load failed: {e}")

st.markdown("---")
st.subheader("🧠 Brainstem Editor")

# Live brain editor
with st.form("brain_editor_form"):
    current_code = get_brain_code()
    edited_code = st.text_area("Edit brainstem.py content below:", current_code, height=400)
    submitted = st.form_submit_button("💾 Save Brain Changes")

    if submitted:
        try:
            save_brain_code(edited_code)
            st.success("Brain code saved successfully. Changes will apply on next run.")
        except Exception as e:
            st.error(f"Failed to save brain: {e}")

st.markdown("---")
st.caption("BlueJay AI Admin Console © 2025")
