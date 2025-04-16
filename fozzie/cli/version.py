import click
from fozzie.version.version_manager import VersionManager

@click.group()
@click.option('--db-path', default=None, help="Optional path to override default fozzie.db location.")
@click.pass_context
def version(ctx, db_path):
    """Manage and view the Fozzie database version."""
    ctx.ensure_object(dict)
    ctx.obj["manager"] = VersionManager(db_path=db_path)

@version.command()
@click.pass_context
def show(ctx):
    """Display the current version."""
    vm = ctx.obj["manager"]
    click.echo(f"📦 Fozzie DB Version: {vm.get_version()}")

@version.command()
@click.pass_context
def minor(ctx):
    """Increment the minor version (e.g., 0.7 → 0.8)."""
    vm = ctx.obj["manager"]
    vm.increment_minor()
    click.secho(f"🔼 Minor version incremented: {vm.get_version()}", fg="green")

@version.command()
@click.pass_context
def major(ctx):
    """Increment the major version (e.g., 0.7 → 1.0)."""
    vm = ctx.obj["manager"]
    vm.increment_major()
    click.secho(f"🚀 Major version incremented: {vm.get_version()}", fg="cyan")

@version.command("init")
@click.argument("db_path", type=click.Path())
@click.option("--version", default=0.1, type=float, help="Initial version number (default: 0.1)")
def init_version(db_path, version):
    """Initialize a new SQLite DB with the version table."""
    try:
        VersionManager.create_new_database(db_path, version)
        click.secho(f"✅ New database created at {db_path} with version {version}", fg="green")
    except FileExistsError as e:
        click.secho(f"❌ {e}", fg="red")




# import click
# from fozzie.version.version_manager import VersionManager

# @click.group()
# @click.option('--db-path', default=None, help="Optional path to override default fozzie.db location.")
# @click.pass_context
# def version(ctx, db_path):
#     """Manage and view the Fozzie database version."""
#     ctx.ensure_object(dict)
#     ctx.obj["manager"] = VersionManager(db_path=db_path)

# @version.command()
# @click.pass_context
# def show(ctx):
#     """Display the current version."""
#     vm = ctx.obj["manager"]
#     click.echo(f"📦 Fozzie DB Version: {vm.get_version()}")

# @version.command()
# @click.pass_context
# def minor(ctx):
#     """Increment the minor version (e.g., 0.7 → 0.8)."""
#     vm = ctx.obj["manager"]
#     vm.increment_minor()
#     click.secho(f"🔼 Minor version incremented: {vm.get_version()}", fg="green")

# @version.command()
# @click.pass_context
# def major(ctx):
#     """Increment the major version (e.g., 0.7 → 1.0)."""
#     vm = ctx.obj["manager"]
#     vm.increment_major()
#     click.secho(f"🚀 Major version incremented: {vm.get_version()}", fg="cyan")

# @version.command("init")
# @click.argument("db_path", type=click.Path())
# @click.option("--version", default=0.1, type=float, help="Initial version number (default: 0.1)")
# def init_version(db_path, version):
#     """Initialize a new SQLite DB with the version table."""
#     try:
#         VersionManager.create_new_database(db_path, version)
#         click.secho(f"✅ New database created at {db_path} with version {version}", fg="green")
#     except FileExistsError as e:
#         click.secho(f"❌ {e}", fg="red")

# # import click
# # from fozzie.version import VersionManager


# # @click.command()
# # @click.argument("action", type=click.Choice(["show", "minor", "major"], case_sensitive=False))
# # @click.option("--db-path", default=None, help="Optional path to the SQLite DB file.")
# # def version(action, db_path):
# #     """Manage the Fozzie DB version.

# #     ACTION must be one of: show, minor, major.
# #     """
# #     vm = VersionManager(db_path=db_path)

# #     if action == "show":
# #         version = vm.get_version()
# #         click.echo(f"📦 Current version: {version}")
# #     elif action == "minor":
# #         vm.increment_minor()
# #         version = vm.get_version()
# #         click.echo(f"✅ Minor version incremented → now at {version}")
# #     elif action == "major":
# #         vm.increment_major()
# #         version = vm.get_version()
# #         click.echo(f"✅ Major version incremented → now at {version}")

# #     vm.close()



# # # import click
# # # from fozzie.version.manager import VersionManager

# # # @click.command()
# # # @click.argument("action", type=click.Choice(["show", "minor", "major"]))
# # # @click.option("--db-path", default=None, help="Path to the SQLite DB")
# # # def version(action, db_path):
# # #     """Manage Fozzie DB version: show, minor, major"""
# # #     vm = VersionManager(db_path=db_path)

# # #     if action == "show":
# # #         click.echo(f"📦 Current version: {vm.get_version()}")
# # #     elif action == "minor":
# # #         vm.increment_minor()
# # #         click.echo("✅ Minor version incremented.")
# # #     elif action == "major":
# # #         vm.increment_major()
# # #         click.echo("✅ Major version incremented (minor reset to 0).")

# # #     vm.close()
