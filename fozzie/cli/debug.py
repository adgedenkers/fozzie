import click
import sys
import os
import platform
from pathlib import Path

@click.command(name="debug")
def debug_command():
    """Run diagnostic checks on the Fozzie CLI environment."""

    click.secho("🐻 Fozzie Doctor - Running system diagnostics...\n", fg="cyan")

    click.echo(f"🧠 Python version:      {platform.python_version()} ({sys.executable})")
    click.echo(f"📁 Working directory:   {os.getcwd()}")
    click.echo(f"📦 PYTHONPATH:          {os.environ.get('PYTHONPATH')}")
    click.echo(f"🧪 Fozzie version:      0.9")

    project_root = Path(__file__).resolve().parents[2]
    fozzie_dir = project_root / "fozzie"
    version_file = fozzie_dir / "version" / "version_manager.py"

    click.echo(f"\n🔍 Checking expected files:")
    click.echo(f" - fozzie path:         {fozzie_dir}")
    click.echo(f" - version manager:     {'✅ Found' if version_file.exists() else '❌ Missing'}")

    # Try an import
    try:
        from fozzie.version.version_manager import VersionManager
        vm = VersionManager()
        version = vm.get_version()
        click.echo(f"\n🧪 VersionManager import: ✅ OK (version = {version})")
    except Exception as e:
        click.secho(f"\n❌ VersionManager import failed: {e}", fg="red")

    click.secho("\n✅ Diagnostics complete.", fg="green")
