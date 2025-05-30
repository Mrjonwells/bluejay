import os
import json
from pytrends.request import TrendReq

def fetch_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["AI", "small business", "ecommerce"], timeframe='now 7-d', geo='US')

    try:
        related = pytrends.related_queries()
        topics = []
        for kw in related.values():
            if kw and kw.get('top') is not None:
                for row in kw['top'].to_dict('records'):
                    if row['query'] not in topics:
                        topics.append(row['query'])
        return topics[:10] if topics else ["AI business tips", "Merchant tools 2025", "Trending AI uses"]
    except Exception as e:
        print("Trend fetch failed:", e)
        return ["AI business tips", "Merchant tools 2025", "Trending AI uses"]

def save_topics(topics):
    output = {"topics": topics}
    path = "backend/seo/external_topics.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(output, f, indent=2)

    # Ensure Git can see the new file
    os.system(f"git add {path}")

def main():
    topics = fetch_google_trends()
    save_topics(topics)
    print("Updated topics:", topics)

if __name__ == "__main__":
    main()
