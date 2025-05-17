import os
import json
from datetime import datetime
from openai import OpenAI

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"

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

def update_sitemap(new_url):
    sitemap_path = "sitemap.xml"
    if not os.path.exists(sitemap_path):
        print("No sitemap.xml found.")
        return

    with open(sitemap_path, "r") as f:
        lines = f.readlines()

    new_entry = f"""  <url>\n    <loc>{new_url}</loc>\n    <priority>0.5</priority>\n  </url>\n"""
    for i, line in enumerate(lines):
        if "</urlset>" in line:
            lines.insert(i, new_entry)
            break

    with open(sitemap_path, "w") as f:
        f.writelines(lines)

    print(f"Sitemap updated with: {new_url}")

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

    # Add to sitemap
    full_url = f"https://askbluejay.ai/blogs/{filename}"
    update_sitemap(full_url)

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = keywords[0]  # Rotate or randomize as needed
    article = generate_article(topic)
    save_post(topic.title(), article)

if __name__ == "__main__":
    run()
