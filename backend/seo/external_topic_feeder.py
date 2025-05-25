import os
import json
from datetime import datetime
from pytrends.request import TrendReq
import requests

OUTPUT_FILE = "backend/seo/external_topics.json"

def fetch_google_trends():
    pytrends = TrendReq()
    pytrends.build_payload(kw_list=["AI", "payment", "small business"])
    trending = pytrends.related_queries()
    keywords = []
    for topic in trending:
        if trending[topic]["top"] is not None:
            keywords += list(trending[topic]["top"]["query"].values)
    return keywords[:10]

def fetch_reddit_titles(subreddits=["smallbusiness", "Entrepreneur"]):
    headers = {"User-Agent": "Mozilla/5.0"}
    titles = []
    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/top/.json?t=day&limit=10"
        try:
            res = requests.get(url, headers=headers)
            posts = res.json()["data"]["children"]
            for post in posts:
                title = post["data"]["title"]
                if len(title.split()) > 3:
                    titles.append(title)
        except Exception as e:
            print(f"Reddit fetch error for /r/{sub}:", e)
    return titles

def save_topics(topics):
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump({"topics": topics, "updated": datetime.utcnow().isoformat()}, f, indent=2)

def main():
    google = fetch_google_trends()
    reddit = fetch_reddit_titles()
    all_topics = sorted(set(google + reddit))
    save_topics(all_topics)
    print(f"Saved {len(all_topics)} topics to external_topics.json")

if __name__ == "__main__":
    main()
