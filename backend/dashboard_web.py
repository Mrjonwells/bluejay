import os
import redis
import requests
import streamlit as st
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Page setup
st.set_page_config(page_title="BlueJay Admin Console", layout="wide")
st.markdown("<h1 style='color:#00aaff;'>📊 BlueJay Admin Console</h1>", unsafe_allow_html=True)
st.markdown("---")

# Redis status check
redis_status = "Unknown"
redis_url = os.getenv("REDIS_URL")
try:
    redis_client = redis.from_url(redis_url, socket_connect_timeout=5)
    redis_client.ping()
    redis_status = "Connected"
except Exception as e:
    redis_status = f"Redis Connection Failed: {e}"
    st.exception(e)

if "Connected" in redis_status:
    st.success("✅ Redis Connected")
else:
    st.error(f"❌ {redis_status}")

# Cost metrics
def fetch_openai_usage():
    key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    now = datetime.utcnow().isoformat()
    month_start = f"{datetime.utcnow():%Y-%m}-01T00:00:00Z"
    res = requests.get(f"https://api.openai.com/v1/dashboard/billing/usage?start_date={month_start}&end_date={now}", headers=headers)
    return round(res.json().get("total_usage", 0) / 100.0, 2)

def fetch_openai_limit():
    key = os.getenv("OPENAI_API_KEY")
    headers = {"Authorization": f"Bearer {key}"}
    res = requests.get("https://api.openai.com/v1/dashboard/billing/subscription", headers=headers)
    return res.json().get("hard_limit_usd", 0)

def fetch_render_cost():
    return 12.00  # static

def fetch_github_actions_cost():
    token = os.getenv("GITHUB_TOKEN")
    repo = "Mrjonwells/bluejay"
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"https://api.github.com/repos/{repo}/actions/runs", headers=headers)
    runs = res.json().get("workflow_runs", [])
    return round(len(runs) * 0.005, 2)

openai_cost = fetch_openai_usage()
openai_limit = fetch_openai_limit()
render_cost = fetch_render_cost()
github_cost = fetch_github_actions_cost()
total_cost = openai_cost + render_cost + github_cost
total_limit = openai_limit + 25 + 10

# Bar chart
st.markdown("### 💰 Current Spend Overview")
bar_data = {
    "OpenAI": openai_cost,
    "Render": render_cost,
    "GitHub": github_cost,
    "Total": total_cost
}
st.bar_chart(bar_data)

# Usage limits
st.markdown("### 📈 Usage Limits")
st.write(f"**OpenAI:** ${openai_cost} of ${openai_limit}")
st.write(f"**Render:** ${render_cost} of $25")
st.write(f"**GitHub Actions:** ${github_cost} of $10")
st.write(f"**Total Usage:** ${total_cost} of ${total_limit}")

st.markdown("---")
st.caption("BlueJay AI Admin Console © 2025")
