import os
import json
import random
import requests

# Load SerpAPI Key
SERP_API_KEY = os.getenv("SERP_API_KEY")

# Paths
SEO_PATH = "backend/seo/seo_config.json"
INSPIRATION_PATH = "backend/generators/blog_inspiration.txt"

def load_random_keyword():
    if not os.path.exists(SEO_PATH):
        print("SEO config not found.")
        return None

    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    keywords = seo.get("keywords", [])
    return random.choice(keywords) if keywords else None

def scrape_google_results(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERP_API_KEY,
        "engine": "google",
        "num": 10
    }

    try:
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        results = data.get("organic_results", [])

        highlights = []
        for item in results:
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            highlights.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n")
        return highlights
    except Exception as e:
        print("Error scraping:", e)
        return []

def save_highlights(highlights, keyword):
    with open(INSPIRATION_PATH, "w") as f:
        f.write(f"Topic: {keyword}\n\n")
        for line in highlights:
            f.write(line + "\n---\n")
    print(f"Saved {len(highlights)} highlights to {INSPIRATION_PATH}")

def run_scraper():
    keyword = load_random_keyword()
    if not keyword:
        print("No keyword found.")
        return

    print(f"Scraping for topic: {keyword}")
    highlights = scrape_google_results(keyword)
    if highlights:
        save_highlights(highlights, keyword)
    else:
        print("No results found.")

if __name__ == "__main__":
    run_scraper()
