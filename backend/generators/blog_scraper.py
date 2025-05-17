import os
import requests

SERP_API_KEY = os.getenv("SERP_API_KEY")
SEARCH_TERM = "how to reduce credit card processing fees for small businesses"

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

def save_highlights(highlights):
    output_path = "backend/generators/blog_inspiration.txt"
    with open(output_path, "w") as f:
        for line in highlights:
            f.write(line + "\n---\n")
    print(f"Scraped {len(highlights)} highlights to {output_path}")

if __name__ == "__main__":
    scraped = scrape_google_results(SEARCH_TERM)
    if scraped:
        save_highlights(scraped)
    else:
        print("No results found.")
