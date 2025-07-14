
# test_finance_app.py
import unittest
import sqlite3
import os
from finance_app import create_users_table, create_transactions_table, create_budgets_table

DB_NAME = 'finance_app.db'

class TestFinanceAppSetup(unittest.TestCase):
    def setUp(self):
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

    def test_user_table_creation(self):
        create_users_table()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_transaction_table_creation(self):
        create_transactions_table()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

    def test_budget_table_creation(self):
        create_budgets_table()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='budgets'")
        result = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
