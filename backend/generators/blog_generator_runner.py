import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"
BLOG_INDEX = "frontend/blog.html"

def load_keywords():
    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    return seo.get("keywords", [])

def generate_article(topic):
    prompt = f"""
Write a blog post (max 450 words) for small business owners on the topic: "{topic}".
Use a helpful, persuasive tone. Mention how AskBlueJay.ai helps lower merchant processing fees.
Start with a punchy intro. Close with a clear call-to-action. Avoid repetition.
Return only the body content. We'll wrap it in HTML later.
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
<body class="blog-page">
  <div class="blog-post">
    <h1>{title}</h1>
    <p><em>Published {date_str}</em></p>
    <div class="content">
      {content.replace(chr(10), '<br><br>')}
    </div>
  </div>
</body>
</html>"""

    os.makedirs(BLOG_OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Blog saved: {filepath}")
    return filename, title, content, date_str

def update_blog_index(entries):
    header = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BlueJay’s Blog</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="blog-index">
<h1>BlueJay’s Blog</h1>
<p>Insights on saving money, merchant processing, and modern tools for small businesses.</p>
<ul>
"""
    links = "".join([
        f"<li><a href=\"blogs/{e[0]}\">{e[1]}</a><br><em>{e[3]} – {e[2][:180].strip()}...</em></li>\n"
        for e in entries
    ])
    footer = "</ul>\n</div>\n</body>\n</html>"

    with open(BLOG_INDEX, "w") as f:
        f.write(header + links + footer)

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = keywords[0]
    article = generate_article(topic)
    filename, title, content, date_str = save_post(topic.title(), article)
    update_blog_index([(filename, title, content, date_str)])
    print(f"Updated blog index with: {title}")
    os.system("bash sync_and_push.sh")

if __name__ == "__main__":
    run()
