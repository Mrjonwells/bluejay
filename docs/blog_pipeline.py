import os
import sys
import json
import re
from datetime import datetime

# Add project root to path to import blog_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.blog_engine import get_trending_topic, generate_blog_content

BLOG_DIR = "docs/blogs"
INDEX_FILE = os.path.join(BLOG_DIR, "index.json")

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def load_index():
    if not os.path.exists(INDEX_FILE):
        return []
    with open(INDEX_FILE, "r") as f:
        return json.load(f)

def save_index(index):
    with open(INDEX_FILE, "w") as f:
        json.dump(index, f, indent=2)

def build_html(title, content, meta, filename):
    date = datetime.utcnow().strftime("%Y-%m-%d")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | AskBlueJay.ai</title>
  <meta name="description" content="{meta['description']}" />
  <meta name="keywords" content="{', '.join(meta['keywords'])}" />
  <meta name="author" content="AskBlueJay.ai" />
  <meta name="robots" content="index, follow" />
  <link rel="stylesheet" href="../style.css" />
  <link rel="canonical" href="https://askbluejay.ai/blogs/{filename}" />
  <meta property="og:title" content="{title} | AskBlueJay.ai" />
  <meta property="og:description" content="{meta['description']}" />
  <meta property="og:image" content="https://askbluejay.ai/logo.png" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="https://askbluejay.ai/blogs/{filename}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title} | AskBlueJay.ai" />
  <meta name="twitter:description" content="{meta['description']}" />
  <meta name="twitter:image" content="https://askbluejay.ai/logo.png" />
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    "headline": "{title}",
    "image": "https://askbluejay.ai/logo.png",
    "author": {{
      "@type": "Organization",
      "name": "AskBlueJay.ai"
    }},
    "publisher": {{
      "@type": "Organization",
      "name": "AskBlueJay.ai",
      "logo": {{
        "@type": "ImageObject",
        "url": "https://askbluejay.ai/logo.png"
      }}
    }},
    "mainEntityOfPage": {{
      "@type": "WebPage",
      "@id": "https://askbluejay.ai/blogs/{filename}"
    }},
    "datePublished": "{date}",
    "description": "{meta['description']}"
  }}
  </script>
</head>
<body>
  <header>
    <img src="../logo.png" alt="BlueJay Logo" class="centered-logo" />
    <nav class="dropdown">
      <button class="dropbtn"><img src="../menu-icon.png" alt="Menu" class="menu-icon" /></button>
      <div class="dropdown-content">
        <a href="../index.html">Home</a>
        <a href="../blog.html">Blog</a>
        <a href="https://calendly.com/askbluejay">Connect</a>
        <a href="../legal.html">Legal</a>
      </div>
    </nav>
  </header>

  <main class="blog-index">
    <article>
      <h1>{title}</h1>
      <p class="date">Published on {date}</p>
      {content}
    </article>
    <section class="share-links" style="text-align:center; margin-top:2em;">
      <p><strong>Share this:</strong></p>
      <a href="https://twitter.com/intent/tweet?text={title}&url=https://askbluejay.ai/blogs/{filename}" target="_blank">Twitter</a> |
      <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://askbluejay.ai/blogs/{filename}" target="_blank">LinkedIn</a>
    </section>
  </main>

  <footer>
    <p>BlueJay and AskBlueJay.ai are property of Fortified Capital LLC. All rights reserved.</p>
  </footer>
</body>
</html>"""

def main():
    topic = get_trending_topic()["rewritten_topic"]
    result = generate_blog_content({"topic": topic})
    filename = f"{datetime.utcnow().strftime('%Y%m%d')}-{slugify(topic)}.html"
    html = build_html(topic, result["content"], result["meta"], filename)

    with open(os.path.join(BLOG_DIR, filename), "w") as f:
        f.write(html)

    index = load_index()
    index.insert(0, {
        "title": topic,
        "filename": filename,
        "description": result["meta"]["description"],
        "keywords": result["meta"]["keywords"],
        "date": datetime.utcnow().isoformat()
    })
    save_index(index)
    print(f"Blog saved: {filename}")

if __name__ == "__main__":
    main()
