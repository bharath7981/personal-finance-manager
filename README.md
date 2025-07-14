#Personal Finance Manager (Command-Line App)

This is a simple and effective command-line application built in Python to help users manage their personal finances. It allows users to register, log in, track income and expenses, set monthly budgets, and generate financial reports.

#Features:
-  User Registration and Login
-  Add, View, Update, and Delete Transactions
-  Categorize income and expenses (e.g., Food, Rent, Salary)
-  Monthly and Yearly Financial Reports
-  Set Budgets by Category and Month
-  Warns when budget limits are exceeded
-  SQLite database for persistent storage
-  Unit tests included for core functionality

#Technologies Used:

- Python 3**
- SQLite3** (built-in)
- unittest** for testing

#Installation:
1. Clone this repository or download the ZIP:
   ```bash
   git clone https://github.com/your-username/personal-finance-manager.git
   cd personal-finance-manager
Run the application:

bash
Copy
Edit
python finance_app.py
 *Make sure Python 3 is installed on your system.

#How to Use:
-Register with a new username and password.

-Log in with your credentials.

-Choose actions from the transaction menu:

-Add income or expense

-View, update, or delete transactions

-Set a monthly budget per category

-Generate reports

-Exit to save all data (stored locally in finance_app.db).

#Example:
markdown
Copy
Edit
Main Menu:
1. Register
2. Login
3. Exit

#Transaction Menu:
1. Add Transaction
2. View Transactions
3. Update Transaction
4. Delete Transaction
5. Generate Financial Report
6. Set Budget
7. Logout

#Testing:
Unit tests are included to verify the database tables are created correctly.
Run tests using:
bash
Copy
Edit
python test_finance_app.py

#File Structure
bash
Copy
Edit
├── finance_app.py          # Main application
├── test_finance_app.py     # Unit tests
├── finance_app.db          # SQLite DB (auto-created)
└── README.md               # Project documentation

#Future Improvements:
Add GUI using Tkinter or PyQt

Export reports to PDF/CSV

Add authentication encryption

Track recurring payments or auto-reminders

