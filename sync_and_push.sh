#!/bin/bash

cd "$(dirname "$0")"

echo "✅ Adding blog and index files..."

mkdir -p frontend/blogs/
find frontend/blogs/ -name '*.html' -exec git add {} \;
[ -f frontend/blog.html ] && git add frontend/blog.html

git config user.name "BlueJay Bot"
git config user.email "bot@askbluejay.ai"

if ! git diff --cached --quiet; then
  echo "🚀 Committing all updates..."
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
else
  echo "Nothing to commit."
fi

# Add fallback for rebase pull issues
echo "🔄 Pulling latest from GitHub..."
git fetch origin main || echo "Fetch failed"
git reset --hard origin/main || echo "Hard reset failed"

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Sync complete."
