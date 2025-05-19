#!/bin/bash

echo "✅ Adding blog and index files..."

# Ensure we're in the right place
cd "$(dirname "$0")"

# Set Git user identity for commit
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# Add blog files
find frontend/blogs/ -name "*.html" -exec git add {} \;
git add frontend/blog.html

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "🔄 Pulling latest from GitHub..."
git pull --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push || echo "Push failed."

echo "✅ Sync complete."
