#!/bin/bash
echo "Building SEO head injection..."

SEO_JSON="backend/seo/seo_config.json"
INJECT_FILE="backend/seo/seo_injection.html"
HTML_FILE="index.html"

# Extract fields from JSON
TITLE=$(jq -r '.title' "$SEO_JSON")
DESCRIPTION=$(jq -r '.meta_description' "$SEO_JSON")
KEYWORDS=$(jq -r '.keywords | join(", ")' "$SEO_JSON")

# Build injection content
cat <<EOF > "$INJECT_FILE"
<title>$TITLE</title>
<meta name="description" content="$DESCRIPTION">
<meta name="keywords" content="$KEYWORDS">
<link rel="canonical" href="https://askbluejay.ai/">
<meta name="robots" content="index, follow">
<meta property="og:title" content="$TITLE" />
<meta property="og:description" content="$DESCRIPTION" />
<meta property="og:url" content="https://askbluejay.ai/" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="$TITLE" />
<meta name="twitter:description" content="$DESCRIPTION" />
EOF

# Inject SEO into HTML file between SEO-INJECT markers
sed -i.bak "/<!-- SEO-INJECT-START -->/,/<!-- SEO-INJECT-END -->/c\
<!-- SEO-INJECT-START -->\n$(cat $INJECT_FILE)\n<!-- SEO-INJECT-END -->
" "$HTML_FILE"

echo "SEO injection complete."
