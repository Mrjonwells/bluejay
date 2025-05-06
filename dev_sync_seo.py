import json
from pytrends.request import TrendReq

SEO_PATH = "backend/seo/seo_config.json"
HTML_PATH = "frontend/index.html"

# Step 1: Fetch trending keywords related to merchant processing
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload(["merchant processing", "Clover POS", "cash discount"], timeframe='now 7-d')
related = pytrends.related_queries()

# Extract top terms
keywords = ["BlueJay", "AI assistant"]
for term in related.values():
    if term["top"] is not None:
        keywords += [entry["query"] for entry in term["top"].head(5).to_dict("records")]

# Step 2: Load existing SEO config
with open(SEO_PATH, "r") as f:
    seo = json.load(f)

seo["keywords"] = sorted(set(keywords))[:12]  # Limit to 12 unique terms

# Step 3: Save updated SEO config
with open(SEO_PATH, "w") as f:
    json.dump(seo, f, indent=2)

# Step 4: Inject updated SEO into index.html
seo_tags = f"""  <title>{seo['title']}</title>
  <meta name="description" content="{seo['meta_description']}" />
  <meta name="keywords" content="{', '.join(seo['keywords'])}" />
  <script type="application/ld+json">
{json.dumps(seo['structured_data'], indent=2)}
  </script>"""

with open(HTML_PATH, "r") as f:
    html = f.read()

start_marker = "<!-- SEO-INJECT-START -->"
end_marker = "<!-- SEO-INJECT-END -->"

before = html.split(start_marker)[0] + start_marker
after = html.split(end_marker)[-1]
new_html = before + "\n" + seo_tags + "\n  " + end_marker + after

with open(HTML_PATH, "w") as f:
    f.write(new_html)

print("✅ SEO updated from Google Trends and injected into index.html")
