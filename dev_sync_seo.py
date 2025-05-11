import json
import os
from pytrends.request import TrendReq
from datetime import datetime

SEO_CONFIG_PATH = "backend/seo/seo_config.json"
TOPICS = ["merchant services", "business processing", "credit card fees", "Clover POS", "Square alternative"]

def fetch_trending_keywords():
    pytrends = TrendReq(hl='en-US', tz=360)
    all_related = []

    for topic in TOPICS:
        try:
            pytrends.build_payload([topic], cat=0, timeframe='now 7-d', geo='US', gprop='')
            related = pytrends.related_queries()[topic]['top']
            if related is not None:
                all_related += [q for q in related['query'].tolist()]
        except Exception:
            continue

    unique_keywords = list(set(all_related))[:20]  # Limit to top 20 unique keywords
    return unique_keywords

def update_seo_file(keywords):
    if not os.path.exists(os.path.dirname(SEO_CONFIG_PATH)):
        os.makedirs(os.path.dirname(SEO_CONFIG_PATH))

    seo_data = {
        "updated": datetime.utcnow().isoformat(),
        "focus_keywords": keywords,
        "meta_title": "BlueJay | Lower Your Processing Fees | Fortified Capital 2025",
        "meta_description": "Discover how BlueJay helps businesses lower credit card fees with cash discount programs and smarter merchant solutions. Backed by Fortified Capital, est. 2025."
    }

    with open(SEO_CONFIG_PATH, "w") as f:
        json.dump(seo_data, f, indent=2)
    print("SEO config updated with fresh keywords.")

if __name__ == "__main__":
    keywords = fetch_trending_keywords()
    update_seo_file(keywords)
