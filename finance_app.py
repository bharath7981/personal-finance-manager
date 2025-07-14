
# finance_app.py
import sqlite3
import datetime

def create_users_table():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Additional code follows (omitted for brevity)
# Please refer to the full code in previous responses

if __name__ == '__main__':
    main()
