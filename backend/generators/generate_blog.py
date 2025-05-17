import os
import json
from datetime import datetime
from openai import OpenAI
import random

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"
INSPIRATION_PATH = "backend/generators/blog_inspiration.txt"

def load_keywords():
    if not os.path.exists(SEO_PATH):
        return []
    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    return seo.get("keywords", [])

def load_inspiration():
    if not os.path.exists(INSPIRATION_PATH):
        return ""
    with open(INSPIRATION_PATH, "r") as f:
        return f.read()

def generate_article(topic, inspiration_text):
    prompt = f"""
Write a 600-word blog post for small business owners on the topic: "{topic}".
Use a helpful, persuasive tone. Mention how AskBlueJay.ai helps lower merchant processing fees.

Here are some excerpts from other top articles on this topic for context:
{inspiration_text}

Include a short intro, body, and a strong CTA at the end.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_post(title, content):
    safe_title = title.lower().replace(" ", "-").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{safe_title}.html"
    filepath = os.path.join(BLOG_OUTPUT_DIR, filename)

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

    os.makedirs(BLOG_OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Blog saved: {filepath}")

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = random.choice(keywords)
    inspiration = load_inspiration()
    article = generate_article(topic, inspiration)
    save_post(topic.title(), article)

if __name__ == "__main__":
    run()
