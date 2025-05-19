#!/bin/bash

cd "$(dirname "$0")"

# 1. Ensure Git identity is configured
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# 2. Generate the blog and update the index
python3 backend/generators/blog_generator_runner.py

# 3. Check out the main branch explicitly
git checkout main

# 4. Stage changes
git add frontend/blogs/ frontend/blog.html

# 5. Only commit if there are changes
if ! git diff --cached --quiet; then
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
  git push https://x-access-token:${BLUEJAY_PAT}@github.com/Mrjonwells/bluejay.git main
else
  echo "No changes to commit."
fi
