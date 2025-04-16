# fozzie/tools/git/setup.py

import os
import subprocess
from dotenv import load_dotenv

def setup_github_env(force: bool = False):
    """Configures Git from .env variables"""
    load_dotenv()

    username = os.getenv("GITHUB_USERNAME")
    email = os.getenv("GITHUB_EMAIL")

    if not username or not email:
        raise ValueError("Missing GITHUB_USERNAME or GITHUB_EMAIL in .env")

    # Set git global config
    subprocess.run(["git", "config", "--global", "user.name", username], check=True)
    subprocess.run(["git", "config", "--global", "user.email", email], check=True)

    print(f"✅ Git configured as: {username} <{email}>")

    if force:
        pat = os.getenv("GITHUB_PAT")
        if not pat:
            raise ValueError("Missing GITHUB_PAT for --force mode")
        print("ℹ️ You can now use this token in HTTPS remotes or GitHub CLI.")
