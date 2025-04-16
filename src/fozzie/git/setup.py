import os
import subprocess

def configure_git_global(username: str, email: str, github_pat: str):
    """
    Configure global Git username, email, and GitHub PAT using credential store.

    Args:
        username (str): GitHub username.
        email (str): Email associated with GitHub.
        github_pat (str): GitHub Personal Access Token.
    """
    try:
        subprocess.run(["git", "config", "--global", "user.name", username], check=True)
        subprocess.run(["git", "config", "--global", "user.email", email], check=True)
        subprocess.run(["git", "config", "--global", "credential.helper", "store"], check=True)

        credentials_path = os.path.expanduser("~/.git-credentials")
        credentials_line = f"https://{username}:{github_pat}@github.com\n"

        with open(credentials_path, "w") as cred_file:
            cred_file.write(credentials_line)

        print(f"✅ Git configured globally for {username} <{email}>.")
        print(f"🔐 GitHub credentials saved to {credentials_path}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run git config command: {e}")
    except Exception as e:
        print(f"❌ Error during Git configuration: {e}")
