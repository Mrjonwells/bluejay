import os
import json
import datetime
from pathlib import Path

SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"
BLOG_INDEX_PATH = "frontend/blog.html"

def load_keywords():
    with open(SEO_PATH, "r") as f:
        data = json.load(f)
        keywords = data.get("keywords", [])
    return keywords

def rotate_keywords(keywords):
    if not keywords:
        return None, keywords
    topic = keywords.pop(0)
    keywords.append(topic)
    with open(SEO_PATH, "r+") as f:
        data = json.load(f)
        data["keywords"] = keywords
        f.seek(0)
        f.write(json.dumps(data, indent=2))
        f.truncate()
    return topic, keywords

def generate_blog_content(topic):
    date = datetime.datetime.now().strftime("%B %d, %Y")
    title = topic.title()
    hook = f"Discover how {topic} is changing the game for small business payments in 2025."

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
        <p>In today's rapidly evolving payments landscape, small business owners are looking for ways to save on fees and stay ahead. {topic} has emerged as a key solution, enabling merchants to retain more revenue while offering flexible payment options to their customers.</p>
        <p>AI-powered systems like AskBlueJay.ai help automate this transition, guiding businesses toward smarter tools such as Clover POS and zero-cost processing models. These innovations don't just reduce cost — they open the door to seamless onboarding, real-time insights, and next-level efficiency.</p>
        <p>Whether you're running a restaurant, retail shop, or service business, understanding how {topic} can be applied in your operation could mean thousands in savings per year. As 2025 progresses, merchants embracing these tools will have the edge.</p>
        <p>Stick with BlueJay for weekly insights on the best ways to cut fees and win in the payments game.</p>
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

    insertion_index = None
    for i, line in enumerate(lines):
        if "<ul>" in line:
            insertion_index = i + 1
            break

    if insertion_index is not None:
        new_entry = f'  <li><a href="blogs/{filename}">{title}</a><br><small>{hook}</small></li>\n'
        lines.insert(insertion_index, new_entry)

    with open(BLOG_INDEX_PATH, "w") as f:
        f.writelines(lines)

    print(f"Updated blog index with: {title}")

def run():
    keywords = load_keywords()
    topic, updated = rotate_keywords(keywords)
    if not topic:
        print("No valid topic to generate.")
        return
    title, hook, body = generate_blog_content(topic)
    filename, _ = save_blog_file(title, body)
    update_blog_index(filename, title, hook)

if __name__ == "__main__":
    run()
