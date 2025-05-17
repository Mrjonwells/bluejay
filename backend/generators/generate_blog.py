import os
import json
from datetime import datetime
from openai import OpenAI

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "backend/seo/seo_config.json"
BLOG_OUTPUT_DIR = "frontend/blogs"
BLOG_INDEX_PATH = "frontend/blog.html"

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
    safe_title = title.lower().replace(" ", "-").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}-{safe_title}.html"
    filepath = os.path.join(BLOG_OUTPUT_DIR, filename)

    formatted_content = content.replace("\n", "<br><br>")

    html_parts = [
        "<!DOCTYPE html>",
        "<html lang=\"en\">",
        "<head>",
        "  <meta charset=\"UTF-8\">",
        f"  <title>{title} | AskBlueJay Blog</title>",
        f"  <meta name=\"description\" content=\"{title} - powered by AskBlueJay.ai\">",
        "  <link rel=\"stylesheet\" href=\"../style.css\">",
        "</head>",
        "<body>",
        "  <div class=\"blog-post\">",
        f"    <h1>{title}</h1>",
        f"    <p><em>Published {date_str}</em></p>",
        "    <div class=\"content\">",
        f"      {formatted_content}",
        "    </div>",
        "  </div>",
        "</body>",
        "</html>"
    ]

    os.makedirs(BLOG_OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write("\n".join(html_parts))

    print(f"Blog saved: {filepath}")
    return filename, title

def update_blog_index(filename, title):
    rel_path = f"blogs/{filename}"
    new_entry = f'<li><a href="{rel_path}" target="_blank">{title}</a></li>\n'

    if not os.path.exists(BLOG_INDEX_PATH):
        with open(BLOG_INDEX_PATH, "w") as f:
            f.write("\n".join([
                "<!DOCTYPE html>",
                "<html lang=\"en\">",
                "<head>",
                "  <meta charset=\"UTF-8\">",
                "  <title>AskBlueJay Blog</title>",
                "  <link rel=\"stylesheet\" href=\"style.css\">",
                "</head>",
                "<body>",
                "  <h1>AskBlueJay Blog</h1>",
                "  <ul>",
                f"    {new_entry}",
                "  </ul>",
                "</body>",
                "</html>"
            ]))
    else:
        with open(BLOG_INDEX_PATH, "r") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if "<ul>" in line:
                lines.insert(i + 1, new_entry)
                break

        with open(BLOG_INDEX_PATH, "w") as f:
            f.writelines(lines)

    print(f"Updated blog index with: {title}")

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = keywords[0]
    article = generate_article(topic)
    filename, title = save_post(topic.title(), article)
    update_blog_index(filename, title)

if __name__ == "__main__":
    run()
