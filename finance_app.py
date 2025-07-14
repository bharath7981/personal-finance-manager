import sqlite3
import datetime

# ---------------------- DATABASE SETUP ----------------------

def create_users_table():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_transactions_table():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_budgets_table():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            category TEXT NOT NULL,
            year TEXT NOT NULL,
            month TEXT NOT NULL,
            amount REAL NOT NULL,
            UNIQUE(user, category, year, month)
        )
    ''')
    conn.commit()
    conn.close()

# ---------------------- AUTHENTICATION ----------------------

def register():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    username = input("Enter a new username: ")
    password = input("Enter a new password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ Registration successful!")
    except sqlite3.IntegrityError:
        print("❌ Username already exists. Please try a different one.")
    
    conn.close()

def login():
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Welcome back, {username}!")
        return username
    else:
        print("❌ Invalid username or password.")
        return None

# ---------------------- TRANSACTIONS ----------------------

def add_transaction(user):
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    t_type = input("Type (income/expense): ").lower()
    if t_type not in ['income', 'expense']:
        print("❌ Invalid type.")
        return

    category = input("Category (e.g., Food, Rent, Salary): ")
    try:
        amount = float(input("Amount: "))
    except ValueError:
        print("❌ Amount must be a number.")
        return

    date = input("Date (YYYY-MM-DD) [Press Enter for today]: ")
    if not date:
        date = datetime.date.today().isoformat()

    cursor.execute('''
        INSERT INTO transactions (user, type, category, amount, date)
        VALUES (?, ?, ?, ?, ?)
    ''', (user, t_type, category, amount, date))

    # 🚨 Budget Check
    if t_type == 'expense':
        year = date[:4]
        month = date[5:7]

        cursor.execute('''
            SELECT amount FROM budgets
            WHERE user = ? AND category = ? AND year = ? AND month = ?
        ''', (user, category, year, month))
        budget = cursor.fetchone()

        cursor.execute('''
            SELECT SUM(amount) FROM transactions
            WHERE user = ? AND type = 'expense' AND category = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
        ''', (user, category, year, month))
        total_spent = cursor.fetchone()[0] or 0

        if budget and total_spent > budget[0]:
            print(f"⚠️ Warning: You've exceeded your budget for '{category}' this month!")

    conn.commit()
    conn.close()
    print("✅ Transaction added.")

def view_transactions(user):
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions WHERE user = ?", (user,))
    rows = cursor.fetchall()

    if not rows:
        print("ℹ️ No transactions found.")
    else:
        print("\n📋 Your Transactions:")
        for row in rows:
            print(f"ID: {row[0]}, Type: {row[2]}, Category: {row[3]}, Amount: ₹{row[4]}, Date: {row[5]}")

    conn.close()

def update_transaction(user):
    view_transactions(user)
    try:
        tid = int(input("Enter Transaction ID to update: "))
        new_category = input("New Category: ")
        new_amount = float(input("New Amount: "))
    except ValueError:
        print("❌ Invalid input.")
        return

    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE transactions
        SET category = ?, amount = ?
        WHERE id = ? AND user = ?
    ''', (new_category, new_amount, tid, user))

    if cursor.rowcount == 0:
        print("❌ No matching transaction found.")
    else:
        print("🔁 Transaction updated.")

    conn.commit()
    conn.close()

def delete_transaction(user):
    view_transactions(user)
    try:
        tid = int(input("Enter Transaction ID to delete: "))
    except ValueError:
        print("❌ Invalid ID.")
        return

    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = ? AND user = ?", (tid, user))

    if cursor.rowcount == 0:
        print("❌ No matching transaction found.")
    else:
        print("🗑️ Transaction deleted.")

    conn.commit()
    conn.close()

# ---------------------- FINANCIAL REPORTS ----------------------

def generate_financial_report(user):
    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    print("\n📆 Generate Report for:")
    year = input("Enter year (e.g., 2025): ")
    month = input("Enter month (1–12 or press Enter for yearly report): ")

    if month:
        cursor.execute("""
            SELECT type, SUM(amount)
            FROM transactions
            WHERE user = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY type
        """, (user, year, month.zfill(2)))
        print(f"\n📊 Monthly Report for {year}-{month.zfill(2)}")
    else:
        cursor.execute("""
            SELECT type, SUM(amount)
            FROM transactions
            WHERE user = ? AND strftime('%Y', date) = ?
            GROUP BY type
        """, (user, year))
        print(f"\n📊 Yearly Report for {year}")

    data = cursor.fetchall()
    conn.close()

    total_income = 0
    total_expense = 0

    for t_type, total in data:
        if t_type == 'income':
            total_income = total
        elif t_type == 'expense':
            total_expense = total

    savings = total_income - total_expense

    print(f"Total Income: ₹{total_income}")
    print(f"Total Expenses: ₹{total_expense}")
    print(f"💰 Savings: ₹{savings}")

# ---------------------- BUDGETING ----------------------

def set_budget(user):
    category = input("Enter category to set budget for (e.g., Food): ")
    year = input("Enter year (e.g., 2025): ")
    month = input("Enter month (1–12): ").zfill(2)
    try:
        amount = float(input("Set budget amount: ₹"))
    except ValueError:
        print("❌ Invalid amount.")
        return

    conn = sqlite3.connect('finance_app.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO budgets (user, category, year, month, amount)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user, category, year, month)
            DO UPDATE SET amount=excluded.amount
        ''', (user, category, year, month, amount))
        conn.commit()
        print("✅ Budget set successfully.")
    except Exception as e:
        print("❌ Error setting budget:", e)

    conn.close()

# ---------------------- TRANSACTION MENU ----------------------

def transaction_menu(user):
    while True:
        print("\n📊 Transaction Menu:")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Update Transaction")
        print("4. Delete Transaction")
        print("5. Generate Financial Report")
        print("6. Set Budget")
        print("7. Logout")

        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction(user)
        elif choice == '2':
            view_transactions(user)
        elif choice == '3':
            update_transaction(user)
        elif choice == '4':
            delete_transaction(user)
        elif choice == '5':
            generate_financial_report(user)
        elif choice == '6':
            set_budget(user)
        elif choice == '7':
            print("👋 Logging out...")
            break
        else:
            print("❌ Invalid option.")

# ---------------------- MAIN APP ----------------------

def main():
    create_users_table()
    create_transactions_table()
    create_budgets_table()

    print("💰 Welcome to Personal Finance Manager 💰")

    while True:
        print("\nMain Menu:\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                transaction_menu(user)
        elif choice == '3':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == '__main__':
    main()
