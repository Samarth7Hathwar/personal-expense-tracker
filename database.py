import sqlite3
from pathlib import Path

DB_PATH = Path("data/expenses.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def expense_table():
    conn = get_connection()
    
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS expenses (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     amount REAL NOT NULL,
                     category TEXT NOT NULL,
                     note TEXT,
                     date TEXT NOT NULL
                     )
                    """)
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS income(
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     amount REAL NOT NULL,
                     source TEXT NOT NULL,
                     note TEXT,
                     date TEXT NOT NULL
                     )
                     """)
    conn.commit()
    conn.close()
    print("Expenses table created successfully.")

def add_expense(amount, category, note, date):
    conn = get_connection()
    conn.execute("""
                 INSERT INTO expenses (amount, category, note, date)
                 VALUES (?, ?, ?, ?)
                 """, (amount, category, note, date))
    conn.commit()
    conn.close()
    print("Expense added successfully.")

def add_income(amount, source, note, date):
    conn = get_connection()
    conn.execute("""
                 INSERT INTO income (amount, source, note, date)
                 VALUES (?, ?, ?, ?)
                 """, (amount, source, note, date))
    conn.commit()
    conn.close()
    print("Income added successfully.")
    
def get_expenses():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM expenses").fetchall()
    conn.close()
    return cursor

def get_income():
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM income").fetchall()
    conn.close()
    return cursor

def total_expenses():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM expenses
                       """).fetchone()
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total

def today_expenses():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM expenses
                       WHERE date = date('now')
                       """).fetchone()
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total

def week_expenses():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM expenses
                       WHERE date >=date('now', '-6 days')
                       """).fetchone()
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total

def month_expenses():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM expenses
                       WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
                       """).fetchone() 
    # strftime('%Y-%m', date) converts a date like: 2024-06-15 to 2024-06, and strftime('%Y-%m', 'now') converts the current date to the same format, allowing us to compare just the year and month.
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total

def month_income():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM income
                       WHERE strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
                       """).fetchone()
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total

def total_income():
    conn = get_connection()
    row = conn.execute("""
                       SELECT SUM(amount)
                       FROM income
                       """).fetchone()
    conn.close()
    total = row[0]
    if total is None:
        return 0
    return total



def delete_expense(expense_id):
    conn = get_connection()
    conn.execute("""
                 DELETE FROM expenses
                 WHERE id = ?
                 """,(expense_id,)) 
    # The ? is a placeholder. We pass the real ID here: (expense_id,)
    # The comma matters. In Python, a one-value tuple needs a comma.
    conn.commit()
    conn.close()

def delete_income(income_id):
    conn = get_connection()
    conn.execute("""
                 DELETE FROM income
                 WHERE id = ?
                 """,(income_id,)) 
    conn.commit()
    conn.close()
    
def get_daily_spending_summary():
    conn = get_connection()
    cursor = conn.execute("""
                          SELECT date, SUM(amount) AS total
                          FROM expenses
                          GROUP BY date
                          ORDER BY date ASC
                            """).fetchall()
    conn.close()
    return cursor

def get_category_summary():
    conn = get_connection()
    cursor = conn.execute("""
                          SELECT category, SUM(amount) AS total
                          FROM expenses
                          GROUP BY category
                          ORDER BY total DESC
                          """).fetchall()
    conn.close()
    return cursor


if __name__ == "__main__":
    expense_table()
    print(get_expenses())