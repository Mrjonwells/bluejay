import os
import json
from datetime import datetime
from openai import OpenAI, OpenAIError
from pytrends.request import TrendReq
from pathlib import Path

BLOG_FOLDER = Path("frontend/blogs/")
INDEX_FILE = Path("frontend/blog.html")

# Setup
pytrends = TrendReq(hl='en-US', tz=360)

def fetch_trending_keywords():
    try:
        pytrends.build_payload(["merchant services", "cash discount", "credit card processing"], timeframe="now 7-d")
        related = pytrends.related_queries()
        keywords = set()
        for kw in related.values():
            if kw and kw.get("top"):
                for entry in kw["top"]:
                    if entry["value"] > 50:
                        keywords.add(entry["query"])
        return list(keywords)
    except Exception as e:
        print(f"[Fallback] Trending fetch failed: {e}")
        return ["cash discounting", "merchant savings", "eliminate credit card fees"]

def generate_blog(keyword):
    prompt = f"""
Write a professional blog post for small business owners about "{keyword}".
Make it educational, persuasive, and practical. Include a strong title and 2–3 sections.
Format in markdown with the title as the first H1 header.
"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_blog_file(title, content):
    slug = (
        title.lower()
        .replace(" ", "_")
        .replace("-", "_")
        .replace(":", "")
        .replace("'", "")
        .replace('"', "")
    )
    filename = f"{slug}.html"
    filepath = BLOG_FOLDER / filename
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <link rel="stylesheet" href="../style.css" />
</head>
<body>
  <header>
    <a href="../index.html"><img src="../logo.png" class="centered-logo" alt="BlueJay Logo" /></a>
  </header>
  <section class="blog-post">
    {content.replace('\n', '<br />')}
  </section>
  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>"""
    with open(filepath, "w") as f:
        f.write(html)
    return filename, title

def update_blog_index(new_post_filename, title):
    with open(INDEX_FILE, "r") as f:
        index_html = f.read()

    hook = f"""
<div class="blog-preview">
  <a href="blogs/{new_post_filename}">{title}</a>
  <p>{datetime.now().strftime('%B %d, %Y')}</p>
</div>
"""

    if "<!-- %%BLOG_POSTS%% -->" in index_html:
        updated = index_html.replace("<!-- %%BLOG_POSTS%% -->", hook + "\n<!-- %%BLOG_POSTS%% -->")
        with open(INDEX_FILE, "w") as f:
            f.write(updated)
    else:
        print("Missing hook in blog.html")

def main():
    keywords = fetch_trending_keywords()
    main_kw = keywords[0] if keywords else "cash discounting"
    blog = generate_blog(main_kw)
    title_line = blog.split("\n")[0]
    title = title_line.replace("Title:", "").strip("# ").strip()
    filename, clean_title = save_blog_file(clean(title), blog)
    update_blog_index(filename, clean_title)
    print(f"Blog '{clean_title}' posted as {filename}")

def clean(title):
    return title.replace(":", "").replace("'", "").replace('"', "").replace("—", "").replace("–", "").strip()

if __name__ == "__main__":
    main()
