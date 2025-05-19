#!/bin/bash

echo "✅ Adding blog and index files..."

# Stage blog and index files if they exist
find frontend/blogs/ -name '*.html' -exec git add {} \;
[ -f frontend/blog.html ] && git add frontend/blog.html

# Basic git identity setup
git config user.name "BlueJay Bot"
git config user.email "bot@askbluejay.ai"

# Commit if there are staged changes
if ! git diff --cached --quiet; then
  echo "🚀 Committing all updates..."
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
else
  echo "Nothing to commit."
fi

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase --autostash || git reset --hard origin/main || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Sync complete."
