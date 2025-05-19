#!/bin/bash

# Set up Git identity for Render (safe to use here)
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# Run the blog generator
cd backend/generators || exit 1
python3 blog_generator_runner.py || exit 1
cd ../.. || exit 1

# Stage and commit blog files
git add frontend/blogs/ frontend/blog.html || exit 1

# Only commit if there are changes
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
  git push https://x-access-token:${BLUEJAY_PAT}@github.com/Mrjonwells/bluejay.git
else
  echo "No changes to commit."
fi
