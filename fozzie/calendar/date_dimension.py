import sqlite3
from datetime import datetime, timedelta
import holidays
import pandas as pd
from pathlib import Path
import argparse
import swisseph as swe
from fozzie.calendar.school_days import populate_school_day_letters

# Constants
START_DATE = datetime.today().date()
START_DATE = datetime(2025, 3, 27).date()
END_DATE = datetime(2025, 6, 30).date()
US_HOLIDAYS = holidays.US()

EQUINOX_SOLSTICE_DATES = {
    "2025-03-20": "Spring Equinox",
    "2025-06-21": "Summer Solstice",
    "2025-09-22": "Fall Equinox",
    "2025-12-21": "Winter Solstice",
    "2026-03-20": "Spring Equinox",
    "2026-06-21": "Summer Solstice",
    "2026-09-23": "Fall Equinox",
    "2026-12-21": "Winter Solstice",
    "2027-03-20": "Spring Equinox",
    "2027-06-21": "Summer Solstice",
    "2027-09-23": "Fall Equinox",
    "2027-12-21": "Winter Solstice"
}

ECLIPSES = {
    "2024-04-08": "solar",
    "2024-09-18": "lunar",
    "2025-03-14": "solar",
    "2025-09-07": "lunar",
    "2026-02-17": "solar",
    "2026-08-12": "lunar",
    "2026-08-23": "solar",
    "2027-02-06": "lunar",
    "2027-08-02": "solar",
    "2027-08-28": "lunar"
}

def get_zodiac_sign(date: datetime.date) -> str:
    jd = swe.julday(date.year, date.month, date.day)
    lon = swe.calc_ut(jd, swe.SUN)[0][0]
    signs = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]
    return signs[int(lon // 30)]

def load_astrological_data(date: datetime.date):
    date_str = date.strftime("%Y-%m-%d")
    astrological_event = EQUINOX_SOLSTICE_DATES.get(date_str)
    zodiac_sign = get_zodiac_sign(date)
    eclipse_type = ECLIPSES.get(date_str)
    return astrological_event, zodiac_sign, eclipse_type

def build_date_dimension(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS date_dimension (
        date TEXT PRIMARY KEY,
        year INTEGER,
        month INTEGER,
        day INTEGER,
        weekday TEXT,
        dow INTEGER,
        doy INTEGER,
        quarter INTEGER,
        gov_quarter INTEGER,
        is_weekend BOOLEAN,
        is_payday BOOLEAN,
        is_school_day BOOLEAN,
        school_day_letter TEXT,
        day_off_reason TEXT,
        is_school_sports_day BOOLEAN,
        game_location TEXT,
        school_location_detail TEXT,
        is_holiday BOOLEAN,
        holiday_name TEXT,
        religious_event TEXT,
        astrological_event TEXT,
        zodiac_sign TEXT,
        eclipse_type TEXT,
        school_pickup_time TEXT
    );
    """)

    current = START_DATE
    while current <= END_DATE:
        date_str = current.strftime("%Y-%m-%d")
        year, month, day = current.year, current.month, current.day
        weekday = current.strftime("%A")
        dow = (current.weekday() + 1) % 7  # Sunday = 0
        doy = int(current.strftime("%j"))
        quarter = (month - 1) // 3 + 1
        gov_quarter = quarter + 1 if quarter < 4 else 1
        is_weekend = dow >= 6

        is_payday = False
        is_school_day = dow < 6 and current not in US_HOLIDAYS
        day_off_reason = None if is_school_day else "Holiday or Weekend"
        is_sports_day = False
        game_location = None
        school_location_detail = None
        school_pickup_time = f"{date_str}T14:30:00" if is_school_day else None

        is_holiday = current in US_HOLIDAYS
        holiday_name = US_HOLIDAYS.get(current) if is_holiday else None
        religious_event = None

        astrological_event, zodiac_sign, eclipse_type = load_astrological_data(current)

        cursor.execute("""
        INSERT OR REPLACE INTO date_dimension VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            date_str, year, month, day, weekday, dow, doy,
            quarter, gov_quarter,
            is_weekend, is_payday, is_school_day, None, day_off_reason,
            is_sports_day, game_location, school_location_detail,
            is_holiday, holiday_name, religious_event,
            astrological_event, zodiac_sign, eclipse_type,
            school_pickup_time
        ))

        current += timedelta(days=1)

    conn.commit()
    conn.close()

    # Populate school day letters
    populate_school_day_letters(db_path, START_DATE.isoformat(), END_DATE.isoformat())

def load_school_data(path: str, db_path: str):
    df = pd.read_excel(path) if path.endswith(".xlsx") else pd.read_csv(path)
    conn = sqlite3.connect(db_path)
    df.to_sql("schools", conn, if_exists="replace", index=False)
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="Build the date_dimension table in a SQLite database.")
    parser.add_argument("--db", type=str, default="calendar.db", help="Path to SQLite database file")
    parser.add_argument("--schools", type=str, help="Path to schools CSV or Excel file")
    args = parser.parse_args()

    Path(args.db).unlink(missing_ok=True)
    build_date_dimension(args.db)
    if args.schools:
        load_school_data(args.schools, args.db)

if __name__ == "__main__":
    main()


# import sqlite3
# from datetime import datetime, timedelta
# import holidays
# import pandas as pd
# from pathlib import Path
# import argparse
# import swisseph as swe
# from fozzie.calendar.school_days import populate_school_day_letters

# # Constants
# START_DATE = datetime.today().date()
# START_DATE = datetime(2025, 3, 27).date()
# END_DATE = datetime(2025, 6, 30).date()
# US_HOLIDAYS = holidays.US()

# EQUINOX_SOLSTICE_DATES = {
#     "2025-03-20": "Spring Equinox",
#     "2025-06-21": "Summer Solstice",
#     "2025-09-22": "Fall Equinox",
#     "2025-12-21": "Winter Solstice",
#     "2026-03-20": "Spring Equinox",
#     "2026-06-21": "Summer Solstice",
#     "2026-09-23": "Fall Equinox",
#     "2026-12-21": "Winter Solstice",
#     "2027-03-20": "Spring Equinox",
#     "2027-06-21": "Summer Solstice",
#     "2027-09-23": "Fall Equinox",
#     "2027-12-21": "Winter Solstice"
# }

# ECLIPSES = {
#     "2024-04-08": "solar",
#     "2024-09-18": "lunar",
#     "2025-03-14": "solar",
#     "2025-09-07": "lunar",
#     "2026-02-17": "solar",
#     "2026-08-12": "lunar",
#     "2026-08-23": "solar",
#     "2027-02-06": "lunar",
#     "2027-08-02": "solar",
#     "2027-08-28": "lunar"
# }

# def get_zodiac_sign(date: datetime.date) -> str:
#     jd = swe.julday(date.year, date.month, date.day)
#     lon = swe.calc_ut(jd, swe.SUN)[0][0]
#     signs = [
#         "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
#         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
#     ]
#     return signs[int(lon // 30)]

# def load_astrological_data(date: datetime.date):
#     date_str = date.strftime("%Y-%m-%d")
#     astrological_event = EQUINOX_SOLSTICE_DATES.get(date_str)
#     zodiac_sign = get_zodiac_sign(date)
#     eclipse_type = ECLIPSES.get(date_str)
#     return astrological_event, zodiac_sign, eclipse_type

# def build_date_dimension(db_path: str):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS date_dimension (
#         date TEXT PRIMARY KEY,
#         year INTEGER,
#         month INTEGER,
#         day INTEGER,
#         weekday TEXT,
#         dow INTEGER,
#         doy INTEGER,
#         quarter INTEGER,
#         gov_quarter INTEGER,
#         is_weekend BOOLEAN,
#         is_payday BOOLEAN,
#         is_school_day BOOLEAN,
#         school_day_letter TEXT,
#         day_off_reason TEXT,
#         is_school_sports_day BOOLEAN,
#         game_location TEXT,
#         school_location_detail TEXT,
#         is_holiday BOOLEAN,
#         holiday_name TEXT,
#         religious_event TEXT,
#         astrological_event TEXT,
#         zodiac_sign TEXT,
#         eclipse_type TEXT,
#         school_pickup_time TEXT
#     );
#     """)

#     current = START_DATE
#     while current <= END_DATE:
#         date_str = current.strftime("%Y-%m-%d")
#         year, month, day = current.year, current.month, current.day
#         weekday = current.strftime("%A")
#         dow = (current.weekday() + 1) % 7  # Sunday = 0
#         doy = int(current.strftime("%j"))
#         quarter = (month - 1) // 3 + 1
#         gov_quarter = quarter + 1 if quarter < 4 else 1
#         is_weekend = dow >= 6

#         is_payday = False
#         is_school_day = dow < 6 and current not in US_HOLIDAYS
#         day_off_reason = None if is_school_day else "Holiday or Weekend"
#         is_sports_day = False
#         game_location = None
#         school_location_detail = None
#         school_pickup_time = f"{date_str}T14:30:00" if is_school_day else None

#         is_holiday = current in US_HOLIDAYS
#         holiday_name = US_HOLIDAYS.get(current) if is_holiday else None
#         religious_event = None

#         astrological_event, zodiac_sign, eclipse_type = load_astrological_data(current)

#         cursor.execute("""
#         INSERT OR REPLACE INTO date_dimension VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
#         """, (
#             date_str, year, month, day, weekday, dow, doy,
#             quarter, gov_quarter,
#             is_weekend, is_payday, is_school_day, None, day_off_reason,
#             is_sports_day, game_location, school_location_detail,
#             is_holiday, holiday_name, religious_event,
#             astrological_event, zodiac_sign, eclipse_type,
#             school_pickup_time
#         ))

#         current += timedelta(days=1)

#     conn.commit()
#     conn.close()

#     # Populate school day letters
#     populate_school_day_letters(db_path, START_DATE.isoformat(), END_DATE.isoformat())

# def load_school_data(path: str, db_path: str):
#     df = pd.read_excel(path) if path.endswith(".xlsx") else pd.read_csv(path)
#     conn = sqlite3.connect(db_path)
#     df.to_sql("schools", conn, if_exists="replace", index=False)
#     conn.close()

# def main():
#     parser = argparse.ArgumentParser(description="Build the date_dimension table in a SQLite database.")
#     parser.add_argument("--db", type=str, default="calendar.db", help="Path to SQLite database file")
#     parser.add_argument("--schools", type=str, help="Path to schools CSV or Excel file")
#     args = parser.parse_args()

#     Path(args.db).unlink(missing_ok=True)
#     build_date_dimension(args.db)
#     if args.schools:
#         load_school_data(args.schools, args.db)

# if __name__ == "__main__":
#     main()
