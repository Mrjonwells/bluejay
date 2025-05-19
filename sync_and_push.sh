#!/bin/bash

# Exit on any error
set -e

echo "🔁 Running SEO sync..."
python3 dev_sync_seo.py || echo "SEO sync skipped or failed."

echo "✅ Adding blog and index files..."
git config user.name "BlueJay Bot"
git config user.email "bot@askbluejay.ai"

# Stage only relevant files
git add frontend/blogs/*.html || echo "No blog posts found to add."
git add frontend/blog.html || echo "No index file found."

# Commit if there are staged changes
if ! git diff --cached --quiet; then
  echo "🚀 Committing all updates..."
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
else
  echo "Nothing to commit."
fi

echo "🔄 Pulling latest from GitHub..."
git pull origin main || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push https://$GITHUB_PAT@github.com/Mrjonwells/bluejay.git main || echo "Push failed."
