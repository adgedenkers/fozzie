import sqlite3
from datetime import datetime, timedelta, date

def get_nth_weekday(year, month, weekday, n):
    """Returns the date of the nth weekday (0=Monday) in a given month/year."""
    count = 0
    for day in range(1, 32):
        try:
            d = date(year, month, day)
            if d.weekday() == weekday:
                count += 1
                if count == n:
                    return d
        except ValueError:
            break
    return None

def get_30_day_occurrences(start_date, target_year, target_month):
    """Returns list of 30-day recurrence dates that fall in the target month."""
    results = []
    current = datetime.strptime(start_date, "%m/%d/%Y").date()
    while current < date(target_year, target_month + 1, 1):
        current += timedelta(days=30)
        if current.year == target_year and current.month == target_month:
            results.append(current)
    return results

def get_biweekly_occurrences(start_date, target_year, target_month):
    """Returns bi-weekly recurrence dates that fall in the target month."""
    results = []
    current = datetime.strptime(start_date, "%m/%d/%Y").date()
    while current < date(target_year, target_month + 1, 1):
        current += timedelta(days=14)
        if current.year == target_year and current.month == target_month:
            results.append(current)
    return results

def populate_tracker_for_month(db_path: str, year: int, month: int):
    """Populates the tracker table with expected income and expenses for the target month."""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Insert expenses
    cur.execute("SELECT * FROM expenses_recurring")
    for row in cur.fetchall():
        (id, expense, frequency, dom, bank_name, account, amount,
         category, renewal, loan_mature_date, notes) = row

        try:
            amount = -abs(float(amount))  # Ensure expenses are negative
        except:
            continue

        if frequency.lower() == "monthly":
            try:
                day = int(dom)
                due_date = date(year, month, day)
                cur.execute("""
                    INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                    VALUES (?, 'expense', ?, ?, ?, ?, ?)
                """, (due_date, expense, amount, bank_name, str(account), category))
            except:
                continue

        elif frequency.lower() == "annual" and renewal:
            try:
                renewal_date = datetime.strptime(renewal, "%j").date().replace(year=year)
                if renewal_date.month == month:
                    cur.execute("""
                        INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                        VALUES (?, 'expense', ?, ?, ?, ?, ?)
                    """, (renewal_date, expense, amount, bank_name, str(account), category))
            except:
                continue

        elif frequency.lower() == "30-days" and renewal:
            try:
                occurrences = get_30_day_occurrences(renewal, year, month)
                for d in occurrences:
                    cur.execute("""
                        INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                        VALUES (?, 'expense', ?, ?, ?, ?, ?)
                    """, (d, expense, amount, bank_name, str(account), category))
            except:
                continue

    # Insert income
    cur.execute("SELECT * FROM income_recurring")
    for row in cur.fetchall():
        (id, source, frequency, received, amount, bank_name, account_type) = row
        frequency = frequency.lower()
        try:
            amount = abs(float(amount))  # Ensure income is positive
        except:
            continue

        try:
            if frequency == "monthly":
                day = int(datetime.strptime(received, "%m/%d/%Y").day)
                income_date = date(year, month, day)
                cur.execute("""
                    INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                    VALUES (?, 'income', ?, ?, ?, ?, '')
                """, (income_date, source, amount, bank_name, account_type))

            elif frequency == "2nd-of-month":
                income_date = date(year, month, 2)
                cur.execute("""
                    INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                    VALUES (?, 'income', ?, ?, ?, ?, '')
                """, (income_date, source, amount, bank_name, account_type))

            elif frequency == "3rd-monday":
                income_date = get_nth_weekday(year, month, weekday=0, n=3)
                if income_date:
                    cur.execute("""
                        INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                        VALUES (?, 'income', ?, ?, ?, ?, '')
                    """, (income_date, source, amount, bank_name, account_type))

            elif frequency in ["bi-weekly", "every-other-week"]:
                occurrences = get_biweekly_occurrences(received, year, month)
                for d in occurrences:
                    cur.execute("""
                        INSERT INTO tracker (date, type, source_or_expense, amount, bank_name, account, category)
                        VALUES (?, 'income', ?, ?, ?, ?, '')
                    """, (d, source, amount, bank_name, account_type))
        except:
            continue

    conn.commit()
    conn.close()
