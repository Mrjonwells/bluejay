import requests

def fetch_wikipedia_summary(term):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term.replace(' ', '%20')}"
        res = requests.get(url, timeout=5)
        data = res.json()
        return data.get("extract", "")
    except Exception:
        return ""
