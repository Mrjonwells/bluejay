# blog_pipeline.py

import os
import json
from datetime import datetime
from pytrends.request import TrendReq
from openai import OpenAI
from pathlib import Path

BLOG_DIR = Path("frontend/blogs")
SEO_FILE = Path("frontend/seo_config.json")
SUMMARY_FILE = Path("frontend/blog_summary.json")

def fetch_trending_keywords():
    pytrends = TrendReq()
    try:
        pytrends.build_payload(["merchant services", "cash discount", "credit card fees"], timeframe="now 7-d")
        related = pytrends.related_queries()

        keywords = []
        for topic in related.values():
            top = topic.get("top", {})
            if "query" in top:
                keywords.extend(top["query"])

        if not keywords:
            raise ValueError("No trending keywords returned by Google.")

        return list(set(keywords))[:10]

    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return [
            "cash discount program",
            "AI merchant tools",
            "credit card fee savings",
            "switch from Square",
            "0% processing",
            "Clover migration",
            "tap to pay savings",
            "Stripe alternative",
            "merchant rate cut",
            "BlueJay AI assistant"
        ]

def generate_blog(keyword):
    prompt = f"Write an engaging blog post about '{keyword}' targeting small business owners. Explain how modern AI tools and cash discount processing can save them money. Include a hook, 2-3 paragraph body, and clear takeaway."
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=700
    )
    return response.choices[0].message.content.strip()

def save_blog(title, content):
    date_str = datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("'", "").replace(",", "")
    filename = f"{date_str}-{slug}.md"
    path = BLOG_DIR / filename
    path.write_text(content)

    with open(SUMMARY_FILE, "w") as f:
        json.dump({"title": title, "date": date_str, "summary": content[:200]}, f)

    print(f"Blog saved to {path}")
    return filename

def update_seo_config(keywords):
    seo_data = {"keywords": keywords}
    with open(SEO_FILE, "w") as f:
        json.dump(seo_data, f)
    print("SEO config updated.")

def main():
    keywords = fetch_trending_keywords()
    if not keywords:
        print("No keywords found. Exiting.")
        return

    main_kw = keywords[0]
    blog = generate_blog(main_kw)
    save_blog(main_kw.title(), blog)
    update_seo_config(keywords)

if __name__ == "__main__":
    main()
