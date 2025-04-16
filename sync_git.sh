#!/bin/bash

# Define your repository path
REPO_PATH="/usr/local/src/[repo]"

# Navigate to the repo
cd "$REPO_PATH" || exit

# Git commands to add, commit, and push
git add .
git commit -m "Auto-commit latest ChatGPT updates"
git push origin main
