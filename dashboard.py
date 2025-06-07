import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
RENDER_API_KEY = os.getenv("RENDER_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "Mrjonwells/bluejay"

def fetch_openai_usage():
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    url = "https://api.openai.com/v1/dashboard/billing/usage"
    now = datetime.utcnow().isoformat()
    month_start = f"{datetime.utcnow():%Y-%m}-01T00:00:00Z"
    res = requests.get(f"{url}?start_date={month_start}&end_date={now}", headers=headers)
    usage = res.json().get("total_usage", 0) / 100.0
    return round(usage, 2)

def fetch_openai_limit():
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    res = requests.get("https://api.openai.com/v1/dashboard/billing/subscription", headers=headers)
    return res.json().get("hard_limit_usd", 0)

def fetch_render_cost():
    # Placeholder: Render doesn't offer public cost API. Manually insert.
    return 12.00

def fetch_github_actions_cost():
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/runs"
    res = requests.get(url, headers=headers)
    runs = res.json().get("workflow_runs", [])
    return round(len(runs) * 0.005, 2)  # Rough est. $0.005 per run

def get_all_metrics():
    openai_cost = fetch_openai_usage()
    openai_limit = fetch_openai_limit()
    render_cost = fetch_render_cost()
    github_cost = fetch_github_actions_cost()

    total = round(openai_cost + render_cost + github_cost, 2)

    return {
        "OpenAI": {"cost": openai_cost, "limit": openai_limit},
        "Render": {"cost": render_cost, "limit": 25},
        "GitHub": {"cost": github_cost, "limit": 10},
        "Total": {"cost": total, "limit": openai_limit + 25 + 10}
    }
