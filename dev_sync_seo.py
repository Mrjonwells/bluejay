import json
from datetime import datetime
from pytrends.request import TrendReq

seo_path = "backend/seo/seo_config.json"
index_path = "frontend/index.html"

with open(seo_path, "r") as f:
    seo_data = json.load(f)

# Fetch trending keywords
pytrends = TrendReq()
pytrends.build_payload(["merchant processing", "point of sale", "card fees"], timeframe="now 7-d")
trends = pytrends.related_queries()

top_terms = []
for group in trends.values():
    if group and group["top"] is not None:
        top_terms += group["top"]["query"].head(5).tolist()

keywords = sorted(set(top_terms + seo_data.get("keywords", [])))
meta_block = f"""
<!-- SEO START -->
<title>{seo_data.get('title')}</title>
<meta name="description" content="{seo_data.get('meta_description')}">
<meta name="keywords" content="{', '.join(keywords)}">
<script type="application/ld+json">{json.dumps(seo_data.get("structured_data", {}))}</script>
<!-- SEO END -->
"""

# Inject into index.html
with open(index_path, "r") as f:
    html = f.read()

start = html.find("<!-- SEO START -->")
end = html.find("<!-- SEO END -->") + len("<!-- SEO END -->")

if start != -1 and end != -1:
    html = html[:start] + meta_block + html[end:]
else:
    html = html.replace("</head>", meta_block + "\n</head>")

with open(index_path, "w") as f:
    f.write(html)

print(f"✅ SEO updated with {len(keywords)} keywords on {datetime.now().isoformat()}")
