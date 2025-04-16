import pytest
from click.testing import CliRunner
from fozzie.cli.chorus import chorus
import tempfile
import sqlite3
from datetime import datetime
import os

@pytest.fixture
def chorus_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
        conn = sqlite3.connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS date_dimension (
                date TEXT PRIMARY KEY,
                is_school_day INTEGER,
                has_chorus INTEGER
            )
        """)
        today = datetime.today().strftime("%Y-%m-%d")
        conn.execute("INSERT INTO date_dimension (date, is_school_day, has_chorus) VALUES (?, 1, 1)", (today,))
        conn.commit()
        conn.close()
        yield db_path
        os.remove(db_path)

def test_chorus_today_yes(chorus_db):
    runner = CliRunner()
    result = runner.invoke(chorus, ["today", chorus_db])
    assert "chorus day" in result.output.lower()

def test_chorus_assign_runs(chorus_db):
    runner = CliRunner()
    result = runner.invoke(chorus, ["assign", chorus_db, "2025-09-01", "2025-09-10"])
    assert "Populated school day letters" in result.output
