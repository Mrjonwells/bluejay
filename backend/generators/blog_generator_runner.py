import os
import json
from datetime import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Safe absolute paths
SEO_PATH = os.path.join(os.path.dirname(__file__), "../seo/seo_config.json")
BLOG_OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/blogs"))
BLOG_INDEX = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend/blog.html"))
SYNC_SEO = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../dev_sync_seo.py"))
SYNC_PUSH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../sync_and_push.sh"))

def load_keywords():
    with open(SEO_PATH, "r") as f:
        seo = json.load(f)
    return seo.get("keywords", [])

def rotate_keywords(keywords):
    if len(keywords) > 1:
        topic = keywords.pop(0)
        keywords.append(topic)
        with open(SEO_PATH, "w") as f:
            json.dump({"keywords": keywords}, f, indent=2)
    return keywords[0]

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
    return filename, title, content, date_str

def update_blog_index():
    posts = []
    for fname in sorted(os.listdir(BLOG_OUTPUT_DIR), reverse=True):
        if fname.endswith(".html"):
            with open(os.path.join(BLOG_OUTPUT_DIR, fname)) as f:
                html = f.read()
                title = html.split("<h1>")[1].split("</h1>")[0]
                date = html.split("<em>Published ")[1].split("</em>")[0]
                summary = html.split("<div class=\"content\">")[1][:180].replace("<br><br>", " ").strip()
                posts.append((fname, title, summary, date))

    header = (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\">\n"
        "  <title>BlueJay’s Blog</title>\n"
        "  <link rel=\"stylesheet\" href=\"style.css\">\n"
        "</head>\n"
        "<body>\n"
        "<div class=\"blog-index\">\n"
        "<h1>BlueJay’s Blog</h1>\n"
        "<p>Insights on saving money, merchant processing, and modern tools for small businesses.</p>\n"
        "<ul>\n"
    )
    items = "".join([
        f"<li><a href=\"blogs/{p[0]}\">{p[1]}</a><br><em>{p[3]} – {p[2]}...</em></li>\n"
        for p in posts
    ])
    footer = "</ul>\n</div>\n</body>\n</html>"

    with open(BLOG_INDEX, "w") as f:
        f.write(header + items + footer)

def run():
    keywords = load_keywords()
    if not keywords:
        print("No keywords found.")
        return

    topic = rotate_keywords(keywords)
    article = generate_article(topic)
    filename, title, content, date_str = save_post(topic.title(), article)
    update_blog_index()
    print(f"Updated blog index with: {title}")

    os.system(f"python3 {SYNC_SEO} && bash {SYNC_PUSH}")

if __name__ == "__main__":
    run()