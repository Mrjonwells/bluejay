#!/bin/bash

# Set git identity if not already set
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# Ensure we're in a git repo
if [ ! -d .git ]; then
  echo "Not a git repository. Exiting."
  exit 1
fi

# Create blogs folder if missing
mkdir -p frontend/blogs

echo "✅ Adding blog and index files..."
git add frontend/blogs/*.html frontend/blog.html || true

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || true

echo "🔄 Pulling latest from GitHub..."
git pull --rebase origin main || true

echo "🔼 Pushing to GitHub..."
git push origin main || true

echo "✅ Sync complete."
