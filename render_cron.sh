#!/bin/bash

# Git identity
git config --global user.email "bluejay@askbluejay.ai"
git config --global user.name "BlueJay Bot"

# Run generator
cd backend/generators || exit 1
python3 blog_generator_runner.py || exit 1
cd ../.. || exit 1

# Commit changes
git add frontend/blogs/ frontend/blog.html || exit 1

if ! git diff --cached --quiet; then
  git commit -m "Auto-sync SEO and blog updates from BlueJay"
  git branch -f main origin/main
  git checkout main
  git pull origin main --rebase
  git push https://x-access-token:${BLUEJAY_PAT}@github.com/Mrjonwells/bluejay.git main
else
  echo "No changes to commit."
fi
