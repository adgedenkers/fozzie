import os
from pathlib import Path

TESTS = {
    "tests/cli/test_version.py": r"""
import pytest
from click.testing import CliRunner
from fozzie.cli.version import version
from fozzie.version.version_manager import VersionManager
import os
import tempfile
import sqlite3

@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    vm = VersionManager(db_path=path)
    vm.initialize_db(vm.conn)
    yield path
    vm.close()
    os.remove(path)

def test_version_show(temp_db):
    runner = CliRunner()
    result = runner.invoke(version, ["show", "--db-path", temp_db])
    assert "0.7" in result.output

def test_version_minor_increment(temp_db):
    runner = CliRunner()
    runner.invoke(version, ["minor", "--db-path", temp_db])
    vm = VersionManager(db_path=temp_db)
    assert round(vm.get_version(), 1) == 0.8
    vm.close()

def test_version_major_increment(temp_db):
    runner = CliRunner()
    runner.invoke(version, ["major", "--db-path", temp_db])
    vm = VersionManager(db_path=temp_db)
    assert vm.get_version() == 1.0
    vm.close()
""",

    "tests/cli/test_chorus.py": r"""
import pytest
from click.testing import CliRunner
from fozzie.cli.chorus import chorus
import sqlite3
import tempfile
import os
from datetime import datetime

@pytest.fixture
def chorus_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    conn = sqlite3.connect(path)
    conn.execute(\"""
        CREATE TABLE IF NOT EXISTS date_dimension (
            date TEXT PRIMARY KEY,
            is_school_day INTEGER,
            has_chorus INTEGER,
            school_day_letter TEXT
        )
    \""")
    today = datetime.today().strftime("%Y-%m-%d")
    conn.execute("INSERT INTO date_dimension (date, is_school_day, has_chorus, school_day_letter) VALUES (?, 1, 1, 'A')", (today,))
    conn.commit()
    conn.close()

    yield path
    os.remove(path)

def test_chorus_today_yes(chorus_db):
    runner = CliRunner()
    result = runner.invoke(chorus, ["today", chorus_db])
    assert "chorus day" in result.output.lower()

def test_chorus_assign_runs(chorus_db):
    runner = CliRunner()
    result = runner.invoke(chorus, ["assign", chorus_db, "2025-09-01", "2025-09-10"])
    assert "Populated school day letters" in result.output
"""
}


def write_fixed_tests(force=False):
    for filepath, content in TESTS.items():
        target = Path(filepath)
        if not target.parent.exists():
            print(f"📂 Creating directory: {target.parent}")
            target.parent.mkdir(parents=True)

        if target.exists() and not force:
            print(f"⚠️  {filepath} already exists. Use --force to overwrite.")
        else:
            target.write_text(content.strip() + "\n", encoding="utf-8")
            print(f"✅ Replaced: {filepath}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fix broken Fozzie test files")
    parser.add_argument("--force", action="store_true", help="Overwrite existing test files")
    args = parser.parse_args()
    write_fixed_tests(force=args.force)
