# fozzie/tools/git/setup.py

import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(".env")

def setup_github_env(force: bool = False) -> None:
    """
    Load Git config from .env and apply global Git settings.

    Required .env keys:
    - GITHUB_USER
    - GITHUB_EMAIL

    Optional:
    - GITHUB_PAT (only checked if force=True)
    """
    if not ENV_PATH.exists():
        raise FileNotFoundError(".env file not found in the current directory")

    load_dotenv(dotenv_path=ENV_PATH)

    username = os.getenv("GITHUB_USER")
    email = os.getenv("GITHUB_EMAIL")

    if not username or not email:
        raise ValueError("Missing GITHUB_USER or GITHUB_EMAIL in .env")

    subprocess.run(["git", "config", "--global", "user.name", username], check=True)
    subprocess.run(["git", "config", "--global", "user.email", email], check=True)
    print(f"✅ Git globally configured as: {username} <{email}>")

    if force:
        pat = os.getenv("GITHUB_PAT")
        if not pat:
            raise ValueError("GITHUB_PAT is required for --force mode")
        print("🔐 GitHub PAT loaded for secure actions (not applied automatically).")
