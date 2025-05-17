import os
import json
from datetime import datetime
from openai import OpenAI

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "backend/seo/seo_config.json"
BLOG_DIR = "frontend/blogs"
SITEMAP_PATH = "frontend/sitemap.xml"
BASE_URL = "https://askbluejay.ai/blogs"

def load_keywords():
    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    return seo.get("keywords", [])

def generate_article(topic):
    prompt = f"""
Write a 600-word blog post for small business owners on the topic: "{topic}".
Use a helpful, persuasive tone. Mention how AskBlueJay.ai helps lower merchant processing fees.
Include a short intro, body, and CTA at the end.
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_post(title, content):
    os.makedirs(BLOG_DIR, exist_ok=True)
    safe_title = title.lower().replace(" ", "-").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{safe_title}.html"
    filepath = os.path.join(BLOG_DIR, filename)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title} | AskBlueJay Blog</title>
  <meta name="description" content="{title} - powered by AskBlueJay.ai">
  <link rel="stylesheet" href="../style.css">
</head>
<body>
  <div class="blog-post">
    <h1>{title}</h1>
    <p><em>Published {date_str}</em></p>
    <div class="content">
      {content.replace('\n', '<br><br>')}
    </div>
  </div>
</body>
</html>"""
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Blog saved: {filepath}")
    return filename

def update_sitemap():
    entries = []
    for file in os.listdir(BLOG_DIR):
        if file.endswith(".html"):
            url = f"{BASE_URL}/{file}"
            entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
    <priority>0.5</priority>
  </url>""")

    full_sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""

    with open(SITEMAP_PATH, "w") as f:
        f.write(full_sitemap)
    print(f"Sitemap updated with {len(entries)} blog entries.")

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = keywords[0]
    article = generate_article(topic)
    save_post(topic.title(), article)
    update_sitemap()

if __name__ == "__main__":
    run()
