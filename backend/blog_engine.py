import json
import random
from datetime import datetime
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_trending_topic():
    try:
        with open("backend/seo/external_topics.json", "r") as f:
            data = json.load(f)
            topics = data.get("topics", [])
    except Exception as e:
        print("Trending topic load error:", e)
        topics = []

    if not topics:
        fallback = [
            "Smart automation in eCommerce",
            "Top fintech trends to watch",
            "How AI is reshaping marketing",
            "The role of AI in customer service",
            "AI-powered tools for small businesses",
            "Generative AI in content creation"
        ]
        topics = fallback

    used_path = "backend/seo/topic_history.json"
    try:
        with open(used_path, "r") as f:
            used = json.load(f)
    except:
        used = []

    unused = [t for t in topics if t not in used]
    if not unused:
        used = []
        unused = topics

    picked = random.choice(unused)
    used.append(picked)

    try:
        with open(used_path, "w") as f:
            json.dump(used, f)
    except Exception as e:
        print("History write error:", e)

    return {"rewritten_topic": picked}

def generate_blog_content(topic):
    topic_text = topic if isinstance(topic, str) else topic.get("rewritten_topic", "AI Trends")

    try:
        with open("docs/blogs/index.json", "r") as f:
            blog_index = json.load(f)
            related_links = blog_index[:3]
    except Exception as e:
        print("Index read error:", e)
        related_links = []

    internal_links_html = ""
    for post in related_links:
        internal_links_html += f'<li><a href="{post["url"]}">{post["title"]}</a></li>\n'

    prompt = (
        f"Write a 300-500 word SEO blog post about '{topic_text}' targeting small business owners. "
        f"Include an informative tone, structured paragraphs, and practical insights. "
        f"Add a short list if relevant, and end with a call to action. Use natural language. "
        f"Date: {datetime.utcnow().strftime('%B %d, %Y')}. "
        f"Use these prior blog titles as context: " +
        ", ".join([p["title"] for p in related_links])
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=1024
    )

    body_html = response.choices[0].message.content.strip().replace("\n", "<br>")

    full_html = f"""
    <div class="blog-post">
        <h1>{topic_text}</h1>
        <p class="blog-date">{datetime.utcnow().strftime('%B %d, %Y')}</p>
        <div class="blog-body">{body_html}</div>
        <hr>
        <h3>Related Posts</h3>
        <ul>
            {internal_links_html}
        </ul>
    </div>
    """

    return {
        "title": topic_text,
        "date": datetime.utcnow().strftime('%Y-%m-%d'),
        "body": full_html
    }
