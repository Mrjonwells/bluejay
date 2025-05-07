import json
from pytrends.request import TrendReq

seo_path = "backend/seo/seo_config.json"

# Load current config
try:
    with open(seo_path, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"⚠️ SEO config not found at {seo_path}")
    config = {}

# Pull top trending keywords from Google Trends
pytrends = TrendReq()
pytrends.build_payload(kw_list=["Clover POS", "AI payment", "cash discount"])

try:
    trends = pytrends.related_queries()
    ranked = trends.get("default", {}).get("rankedList", [])
    if ranked and "rankedKeyword" in ranked[0]:
        seo_keywords = [kw["query"] for kw in ranked[0]["rankedKeyword"]]
    else:
        print("⚠️ No ranked keywords found — using fallback list.")
        seo_keywords = ["AI payments", "merchant savings", "Clover POS"]
except Exception as e:
    print(f"⚠️ Pytrends error: {e}")
    seo_keywords = ["AI payments", "merchant savings", "Clover POS"]

# Update SEO config
config["keywords"] = list(set(config.get("keywords", []) + seo_keywords))

# Save updated config
with open(seo_path, "w") as f:
    json.dump(config, f, indent=2)

print("✅ SEO keywords updated.")
