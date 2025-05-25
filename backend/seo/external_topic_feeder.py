import json
from pytrends.request import TrendReq
from datetime import datetime

def fetch_google_trends():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(['AI for business'], cat=0, timeframe='now 7-d', geo='US', gprop='')
    
    try:
        related_queries = pytrends.related_queries()
        results = related_queries.get('AI for business', {}).get('top', {}).get('query', [])
        if not results:
            raise ValueError("No trending results found.")
        return results[:5]
    except Exception as e:
        print("Trend fetch error:", e)
        return ["AI business tools", "automation in business", "AI trends 2025"]

def main():
    topics = fetch_google_trends()
    timestamp = datetime.utcnow().isoformat()
    
    payload = {
        "timestamp": timestamp,
        "topics": topics
    }

    with open("backend/seo/trending_topics.json", "w") as f:
        json.dump(payload, f, indent=2)
    
    print(f"Saved {len(topics)} trending topics.")

if __name__ == "__main__":
    main()
