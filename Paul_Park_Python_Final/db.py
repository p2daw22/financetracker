
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="money_tracker.sqlite"):
        self.db_name = db_name

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        self.create_budget_table()
        self.create_income_table()

    def create_budget_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budget (
            category TEXT,
            allocated REAL,
            spent REAL DEFAULT 0,
            month_year TEXT,
            PRIMARY KEY (category, month_year)
        )
        """)
        conn.commit()
        conn.close()

    def create_income_table(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            amount REAL NOT NULL,
            day TEXT,
            month_year TEXT
        )
        """)
        conn.commit()
        conn.close()

    def add_category_expense(self, category, amount):
        month_year = datetime.now().strftime("%B-%Y")
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE budget
        SET spent = spent + ?
        WHERE category = ? AND month_year = ?
        """, (amount, category, month_year))
        conn.commit()
        conn.close()

    def update_budget(self, category, new_allocated):
        month_year = datetime.now().strftime("%B-%Y")
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE budget
        SET allocated = ?
        WHERE category = ? AND month_year = ?
        """, (new_allocated, category, month_year))
        conn.commit()
        conn.close()

    def update_expense(self, category, new_spent):
        month_year = datetime.now().strftime("%B-%Y")
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE budget
        SET spent = ?
        WHERE category = ? AND month_year = ?
        """, (new_spent, category, month_year))
        conn.commit()
        conn.close()

    def get_budget_status_for_month(self, month_year):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT category, allocated, spent FROM budget WHERE month_year = ?
        """, (month_year,))
        results = cursor.fetchall()
        conn.close()
        return results

    def add_income(self, source, amount):
        month_year = datetime.now().strftime("%B-%Y")
        day = datetime.now().strftime("%d")
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO income (source, amount, day, month_year)
        VALUES (?, ?, ?, ?)
        """, (source, amount, day, month_year))
        conn.commit()
        conn.close()

    def get_income(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, source, amount, month_year FROM income
        """)
        results = cursor.fetchall()
        conn.close()
        return results

    def update_income(self, income_id, new_amount):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE income
        SET amount = ?
        WHERE id = ?
        """, (new_amount, income_id))
        conn.commit()
        conn.close()
