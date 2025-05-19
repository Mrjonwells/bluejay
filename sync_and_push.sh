#!/bin/bash

echo "✅ Adding blog and index files..."

# Try to stage all new/modified blog files, but don’t fail if none exist
find frontend/blogs/ -name "*.html" -exec git add {} \; 2>/dev/null || true
git add frontend/blog.html 2>/dev/null || true

echo "🚀 Committing all updates..."
git commit -m "Auto-sync SEO and blog updates from BlueJay" || echo "Nothing to commit."

echo "✅ Sync complete."
