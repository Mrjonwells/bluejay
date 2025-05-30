import os
from datetime import datetime

BLOG_DIR = "docs/blogs"
SITEMAP_PATH = "docs/sitemap.xml"
BASE_URL = "https://askbluejay.ai/blogs"

def build_entry(filename):
    url = f"{BASE_URL}/{filename}"
    return f"""  <url>
    <loc>{url}</loc>
    <lastmod>{datetime.utcnow().date()}</lastmod>
    <priority>0.5</priority>
  </url>"""

def update_sitemap():
    entries = []
    for file in os.listdir(BLOG_DIR):
        if file.endswith(".html"):
            entries.append(build_entry(file))

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(entries)}
</urlset>"""

    with open(SITEMAP_PATH, "w") as f:
        f.write(sitemap)

    print(f"Sitemap updated with {len(entries)} entries.")

if __name__ == "__main__":
    update_sitemap()
