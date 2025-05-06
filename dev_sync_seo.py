import json

SEO_PATH = "backend/seo/seo_config.json"
HTML_PATH = "frontend/index.html"  # Adjust if yours differs

with open(SEO_PATH, "r") as f:
    seo = json.load(f)

seo_tags = f"""  <title>{seo['title']}</title>
  <meta name="description" content="{seo['meta_description']}" />
  <meta name="keywords" content="{', '.join(seo['keywords'])}" />
  <script type="application/ld+json">
{json.dumps(seo['structured_data'], indent=2)}
  </script>"""

with open(HTML_PATH, "r") as f:
    html = f.read()

new_html = html.replace(
    "<!-- SEO-INJECT-START -->", f"<!-- SEO-INJECT-START -->\n{seo_tags}\n  <!-- SEO-INJECT-END -->"
)

with open(HTML_PATH, "w") as f:
    f.write(new_html)

print("✅ SEO tags synced into index.html")
