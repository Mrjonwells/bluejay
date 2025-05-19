#!/bin/bash

set -e

echo "✅ Adding blog and index files..."

# Move to repo root no matter where script is run from
cd "$(dirname "$0")"

# Ensure we're on the main branch (create if necessary)
git checkout main 2>/dev/null || git checkout -b main

# Add blog posts and index if they exist
git add frontend/blogs/*.html frontend/blog.html 2>/dev/null || echo "No blog files to add."

# Commit only if there are staged changes
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
else
  echo "Nothing to commit."
fi

echo "🔄 Pulling latest from GitHub..."
git pull origin main --rebase || echo "Pull failed (non-blocking)."

echo "🔼 Pushing to GitHub..."
git push origin main || echo "Push failed."

echo "✅ Sync complete."
