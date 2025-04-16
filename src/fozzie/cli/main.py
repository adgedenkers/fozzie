import argparse
from fozzie.cli.chorus import run_chorus_command
from fozzie.cli.version import run_version_command

def main():
    parser = argparse.ArgumentParser(description="Fozzie CLI - 🐻 Developer Tools")
    subparsers = parser.add_subparsers(dest="command")

    # Chorus CLI
    chorus_parser = subparsers.add_parser("chorus", help="Chorus day checker")
    chorus_parser.add_argument("--date", help="Date to check (default: today)")
    chorus_parser.set_defaults(func=run_chorus_command)

    # Version CLI
    version_parser = subparsers.add_parser("version", help="Manage database version")
    version_parser.add_argument("action", choices=["minor", "major", "show"])
    version_parser.add_argument("--db-path", help="Optional path to DB")
    version_parser.set_defaults(func=run_version_command)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()
