import json
from datetime import datetime
from pytrends.request import TrendReq

# Load existing config
with open("backend/seo/seo_config.json", "r") as f:
    seo_data = json.load(f)

# Pull fresh keywords from Google Trends
pytrends = TrendReq()
pytrends.build_payload(["merchant services", "point of sale", "card processing"], timeframe="now 7-d")
trends = pytrends.related_queries()
top_terms = []

for topic in trends.values():
    if topic and topic['top'] is not None:
        top_terms += topic['top']['query'].head(5).tolist()

# Inject keywords into HTML head
with open("frontend/index.html", "r") as f:
    html = f.read()

start = html.find("<!-- SEO START -->")
end = html.find("<!-- SEO END -->") + len("<!-- SEO END -->")

keywords = ", ".join(sorted(set(top_terms)))
meta_block = f"""
<!-- SEO START -->
<title>{seo_data.get('title')}</title>
<meta name="description" content="{seo_data.get('description')}">
<meta name="keywords" content="{keywords}">
<!-- SEO END -->
"""

# Replace old block
if start != -1 and end != -1:
    html = html[:start] + meta_block + html[end:]
else:
    html = html.replace("</head>", meta_block + "\n</head>")

with open("frontend/index.html", "w") as f:
    f.write(html)

print(f"✅ SEO updated with {len(top_terms)} keywords on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
