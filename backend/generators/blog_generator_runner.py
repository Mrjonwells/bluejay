import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
SEO_PATH = "../seo/seo_config.json"
BLOG_OUTPUT_DIR = "../../frontend/blogs"
BLOG_INDEX = "../../frontend/blog.html"

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
    with open(BLOG_INDEX, "r") as f:
        html = f.read()

    ul_start = html.find("<ul>")
    ul_end = html.find("</ul>")
    if ul_start == -1 or ul_end == -1:
        print("Could not find <ul> section in blog index.")
        return

    links = "".join([f"<li><a href=\"blogs/{e[0]}\">{e[1]}</a></li>\n" for e in entries])
    new_html = html[:ul_start + 4] + "\n" + links + html[ul_end:]

    with open(BLOG_INDEX, "w") as f:
        f.write(new_html)

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
