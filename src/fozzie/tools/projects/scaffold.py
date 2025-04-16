# fozzie/tools/project/scaffold.py

import os
from pathlib import Path
import click

SUPPORTED_TYPES = {
    "streamlit": ["app.py", "requirements.txt", ".gitignore"],
    "fastapi": ["main.py", "requirements.txt", ".gitignore"],
    "notebook": ["notebook.ipynb", "requirements.txt", ".gitignore"],
    "pypkg": ["__init__.py", "setup.py", "requirements.txt", ".gitignore"],
    "bash": ["script.sh"],
    "powershell": ["script.ps1"]
}

TEMPLATE_CONTENTS = {
    "app.py": "import streamlit as st\n\nst.title('My Streamlit App')\n",
    "main.py": "from fastapi import FastAPI\n\napp = FastAPI()\n\n@app.get('/')\ndef read_root():\n    return {\"Hello\": \"World\"}\n",
    "notebook.ipynb": "{\"cells\": [], \"metadata\": {}, \"nbformat\": 4, \"nbformat_minor\": 5}",
    "__init__.py": "",
    "setup.py": "from setuptools import setup\n\nsetup(name='my_package', version='0.1')\n",
    "requirements.txt": "",
    ".gitignore": "__pycache__/\n.env\n*.pyc\n",
    "script.sh": "#!/bin/bash\necho 'Hello from Bash'\n",
    "script.ps1": "Write-Host 'Hello from PowerShell'\n"
}

@click.command()
@click.argument('type')
@click.argument('name')
def scaffold(type, name):
    """Scaffold a new project directory."""
    type = type.lower()
    if type not in SUPPORTED_TYPES:
        raise click.ClickException(f"Unsupported project type: {type}")

    project_dir = Path(name)
    project_dir.mkdir(parents=True, exist_ok=True)

    for file in SUPPORTED_TYPES[type]:
        file_path = project_dir / file
        content = TEMPLATE_CONTENTS.get(file, '')
        file_path.write_text(content)

    click.echo(f"Project scaffolded at {project_dir.resolve()}")
