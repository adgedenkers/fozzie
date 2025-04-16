import sqlite3
import datetime
from typing import Optional

def add_school_day_letter_column(db_path: str):
    """
    Adds the 'school_day_letter' column to the 'date_dimension' table if it doesn't exist.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE date_dimension ADD COLUMN school_day_letter TEXT")
    except sqlite3.OperationalError as e:
        if "duplicate column name" not in str(e).lower():
            raise
    finally:
        conn.commit()
        conn.close()

def assign_school_day_letters(db_path: str, start_date: str, end_date: str):
    """
    Assigns alternating "A" and "B" letters to consecutive school days between start_date and end_date.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT date FROM date_dimension 
        WHERE date BETWEEN ? AND ? AND is_school_day = 1 
        ORDER BY date ASC
    """, (start_date, end_date))
    
    dates = [row[0] for row in cur.fetchall()]

    for idx, date in enumerate(dates):
        letter = 'A' if idx % 2 == 0 else 'B'
        cur.execute("""
            UPDATE date_dimension
            SET school_day_letter = ?
            WHERE date = ?
        """, (letter, date))

    conn.commit()
    conn.close()

def populate_school_day_letters(db_path: str, start_date: str, end_date: str):
    """
    Runs add_school_day_letter_column and assign_school_day_letters in one call.
    """
    add_school_day_letter_column(db_path)
    assign_school_day_letters(db_path, start_date, end_date)

def chorus_today(db_path: str, today: Optional[str] = None) -> bool:
    """
    Returns True if today is a chorus day (Wednesday or Thursday AND an "A" day), else False.
    """
    if today is None:
        today_dt = datetime.date.today()
    else:
        today_dt = datetime.datetime.strptime(today, "%Y-%m-%d").date()

    weekday = today_dt.weekday()  # Monday = 0, ..., Sunday = 6
    today_str = today_dt.isoformat()

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
        SELECT is_school_day, school_day_letter
        FROM date_dimension
        WHERE date = ?
    """, (today_str,))

    result = cur.fetchone()
    conn.close()

    if result:
        is_school_day, letter = result
        if is_school_day == 1 and letter == 'A' and weekday in (2, 3):  # Wednesday or Thursday
            return True

    return False
