#!/bin/bash

echo "=== Starting build process ==="

# Step 1: Inject SEO head content from seo_injection.html
echo "Injecting SEO head tags..."
SEO_SNIPPET=$(cat backend/seo/seo_injection.html)
perl -0777 -i -pe "s/<!-- SEO-INJECT-START -->.*?<!-- SEO-INJECT-END -->/<!-- SEO-INJECT-START -->\n$SEO_SNIPPET\n<!-- SEO-INJECT-END -->/s" frontend/index.html

echo "SEO injection complete."

# Step 2: Optional lint or format (disabled for now)
# black backend/  # Uncomment if using Python formatting

echo "=== Build process complete ==="
