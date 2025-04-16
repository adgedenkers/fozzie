# fozzie/cli/__init__.py
import click
from .chorus import chorus
from .version import version
from .debug import debug_command
from .sports import sports



@click.group()
def cli():
    """Fozzie CLI — All your dev tools, one grumpy bear."""
    pass

cli.add_command(chorus)
cli.add_command(version)
cli.add_command(debug_command)
cli.add_command(sports)
