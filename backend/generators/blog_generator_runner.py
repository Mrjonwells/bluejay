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

def rotate_keywords():
    with open(SEO_PATH, "r+") as f:
        data = json.load(f)
        keywords = data.get("keywords", [])
        if not keywords:
            return None
        topic = keywords.pop(0)
        keywords.append(topic)
        f.seek(0)
        json.dump({"keywords": keywords}, f, indent=2)
        f.truncate()
        return topic

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
        <p>{topic} is one of the fastest-evolving areas in the merchant services industry. With new tools and technologies emerging daily, it’s crucial for small businesses to stay ahead of the curve.</p>
        <p>From AI-driven insights to automated fee reductions, {topic} enables business owners to reclaim their margins while improving the customer experience.</p>
        <p>At BlueJay, we believe the future of payments is lean, fast, and intelligent. If you're still paying legacy processing rates, there's a better way — and it starts with understanding these modern trends.</p>
        <p>Stay tuned for more weekly insights.</p>
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

    print(f"Blog saved: {output_path}")
    return filename, title

def update_blog_index(filename, title, hook):
    with open(BLOG_INDEX_PATH, "r") as f:
        lines = f.readlines()

    insertion_point = None
    for i, line in enumerate(lines):
        if "<ul>" in line:
            insertion_point = i + 1
            break

    if insertion_point is not None:
        entry = f'  <li><a href="blogs/{filename}">{title}</a><br><small>{hook}</small></li>\n'
        lines.insert(insertion_point, entry)

        with open(BLOG_INDEX_PATH, "w") as f:
            f.writelines(lines)

        print(f"Updated blog index with: {title}")

def run():
    topic = rotate_keywords()
    if not topic:
        print("No keywords found.")
        return

    title, hook, body = generate_blog_content(topic)
    filename, saved_title = save_blog_file(title, body)
    update_blog_index(filename, saved_title, hook)

if __name__ == "__main__":
    run()
