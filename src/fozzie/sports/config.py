# fozzie/sports/config.py
import os
import tomllib  # Use tomli if Python < 3.11
from pathlib import Path

CONFIG_PATH = Path.home() / ".fozzie" / "config.toml"

def load_sports_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "rb") as f:
        return tomllib.load(f).get("sports", {})

# # fozzie/sports/config.py
# import os
# import tomllib  # Use tomli if Python < 3.11
# from pathlib import Path

# CONFIG_PATH = Path.home() / ".fozzie" / "config.toml"

# def load_sports_config():
#     if not CONFIG_PATH.exists():
#         return {}
#     with open(CONFIG_PATH, "rb") as f:
#         return tomllib.load(f).get("sports", {})