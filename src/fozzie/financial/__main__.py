# fozzie/financial/__main__.py
import argparse
from fozzie.financial.tracker import populate_tracker_for_month

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Populate monthly financial tracker.")
    parser.add_argument("db", help="Path to SQLite database")
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int)
    args = parser.parse_args()

    populate_tracker_for_month(args.db, args.year, args.month)
