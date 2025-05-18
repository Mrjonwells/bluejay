import os
import json
import random
from datetime import datetime
from openai import OpenAI

# Setup
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "../seo/seo_config.json"
BLOG_OUTPUT_DIR = "../../frontend/blogs"
BLOG_INDEX = "../../frontend/blog.html"

def load_keywords():
    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    return seo.get("keywords", [])

def generate_article(topic):
    ctas = [
        "Want to save more on every swipe? Try AskBlueJay.",
        "Curious how much you could keep? Let’s find out together.",
        "Let BlueJay help you cut costs — it’s free to try.",
    ]
    selected_cta = random.choice(ctas)
    prompt = f"""
Write a short blog post (max 350 words) for small business owners on: "{topic}".
Tone: helpful, clear, persuasive.
Structure: 1 intro paragraph, 2 body sections, and a natural final CTA: "{selected_cta}"
Avoid repeating the topic name more than twice. Make it sound human.
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

    html = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        f"  <meta charset=\"UTF-8\">\n"
        f"  <title>{title} | AskBlueJay Blog</title>\n"
        f"  <meta name=\"description\" content=\"{title} - powered by AskBlueJay.ai\">\n"
        "  <link rel=\"stylesheet\" href=\"../style.css\">\n"
        "</head>\n"
        "<body class=\"blog-page\">\n"
        "  <div class=\"blog-post\">\n"
        f"    <h1>{title}</h1>\n"
        f"    <p><em>Published {date_str}</em></p>\n"
        "    <div class=\"content\">\n"
        f"      {content.replace(chr(10), '<br><br>')}\n"
        "    </div>\n"
        "  </div>\n"
        "</body>\n"
        "</html>"
    )

    os.makedirs(BLOG_OUTPUT_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)
    print(f"Blog saved: {filepath}")
    return filename, title

def update_blog_index(entries):
    header = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        "  <title>AskBlueJay Blog</title>\n"
        "  <link rel=\"stylesheet\" href=\"style.css\">\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"blog-index\">\n"
        "<h1>AskBlueJay Blog</h1>\n"
        "<p>Insights on saving money, merchant processing, and modern tools for small businesses.</p>\n"
        "<ul>\n"
    )
    links = "".join([f"<li><a href=\"blogs/{e[0]}\">{e[1]}</a></li>\n" for e in entries])
    footer = "</ul>\n</div>\n</body>\n</html>"

    full_html = header + links + footer
    with open(BLOG_INDEX, "w") as f:
        f.write(full_html)

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = keywords[0]
    article = generate_article(topic)
    filename, title = save_post(topic.title(), article)
    update_blog_index([(filename, title)])
    print(f"Updated blog index with: {title}")

    os.system("bash sync_and_push.sh")

if __name__ == "__main__":
    run()
