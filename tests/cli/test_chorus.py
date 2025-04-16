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
