import os
import json
import datetime
from pathlib import Path

SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"
BLOG_INDEX_PATH = "frontend/blog.html"

def load_keywords():
    with open(SEO_PATH, "r") as f:
        return json.load(f).get("keywords", [])

def generate_blog_content(topic):
    date = datetime.datetime.now().strftime("%B %d, %Y")
    title = topic.title()
    hook = f"Learn how {topic} is transforming the way businesses handle payments in 2025."

    body = f"""
    <html>
    <head>
      <title>{title}</title>
      <link rel="stylesheet" href="../style.css">
    </head>
    <body>
      <div class="blog-post">
        <h1>{title}</h1>
        <p><em>Published on {date}</em></p>
        <p>{hook}</p>
        <p>{topic} is one of the top trends in the merchant processing world right now. Businesses are using it to cut costs, improve efficiency, and gain an edge over competitors.</p>
        <p>BlueJay is here to guide you through these changes with insights, automation, and powerful integrations.</p>
        <p>Stay tuned for more.</p>
      </div>
    </body>
    </html>
    """.strip()
    return title, hook, body

def save_blog_file(title, body):
    slug = datetime.datetime.now().strftime("%Y-%m-%d") + "-" + title.lower().replace(" ", "-")
    filename = f"{slug}.html"
    output_path = os.path.join(BLOG_OUTPUT_DIR, filename)

    Path(BLOG_OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    with open(output_path, "w") as f:
        f.write(body)

    print(f"✅ Blog saved: {output_path}")
    return filename, title

def update_blog_index(filename, title, hook):
    with open(BLOG_INDEX_PATH, "r") as f:
        lines = f.readlines()

    insertion_point = next((i + 1 for i, line in enumerate(lines) if "<ul>" in line), None)

    if insertion_point is not None:
        entry = f'  <li><a href="blogs/{filename}">{title}</a><br><small>{hook}</small></li>\n'
        lines.insert(insertion_point, entry)

        with open(BLOG_INDEX_PATH, "w") as f:
            f.writelines(lines)

        print(f"✅ Updated blog index with: {title}")
    else:
        print("❌ <ul> tag not found in blog index.")

def run():
    keywords = load_keywords()
    if not keywords:
        print("❌ No keywords found.")
        return

    topic = keywords[0]
    title, hook, body = generate_blog_content(topic)
    filename, saved_title = save_blog_file(title, body)
    update_blog_index(filename, saved_title, hook)

if __name__ == "__main__":
    run()
