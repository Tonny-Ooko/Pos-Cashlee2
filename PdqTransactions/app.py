from flask import Flask, render_template, request
import sqlite3
import datetime
import random
import mysql.connector

app = Flask(__name__, template_folder='.')

# SQLite database configuration
DB_FILE = 'transactions.db'

# MySQL database configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'TONNY',
    'password': '123456',
    'database': 'Product'
}


# Function to create SQLite database
def create_sqlite_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                 id INTEGER PRIMARY KEY,
                 timestamp TIMESTAMP NOT NULL,
                 amount REAL NOT NULL,
                 payment_method TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

# Function to create MySQL database
def create_mysql_db():
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS PointSale (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        time_of_transaction VARCHAR(8) NOT NULL,
                        date_of_transaction DATE NOT NULL,
                        day VARCHAR(10) NOT NULL,
                        transaction_code VARCHAR(50) NOT NULL);''')
    connection.commit()
    connection.close()

# Simulating PDQ payment confirmation
def confirm_payment_with_pdq():
    return random.choice([True, False])  # Simulating a random success or failure

# Function to parse transaction details from the PDQ message
def parse_transaction_details(message):
    # Assuming the message contains transaction code, username, time, and date
    # Replace the parsing logic below with the actual parsing based on your message format
    transaction_code = "123456"  # Replace with the actual parsed value
    username = "John Doe"  # Replace with the actual parsed value
    time_of_transaction = "12:34:56"  # Replace with the actual parsed value
    date_of_transaction = "2023-07-30"  # Replace with the actual parsed value
    return transaction_code, username, time_of_transaction, date_of_transaction

# Function to insert user details into MySQL database
def insert_user_details_into_mysql(username, time_of_transaction, date_of_transaction, transaction_code):
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()
    day_of_week = datetime.datetime.strptime(date_of_transaction, "%Y-%m-%d").strftime('%A')
    insert_query = '''INSERT INTO PointSale (username, time_of_transaction, date_of_transaction, day, transaction_code)
                      VALUES (%s, %s, %s, %s, %s)'''
    insert_values = (username, time_of_transaction, date_of_transaction, day_of_week, transaction_code)
    cursor.execute(insert_query, insert_values)
    connection.commit()
    connection.close()

# Function to process PDQ transaction
def process_pdq_transaction(message):
    pdq_payment_confirmed = confirm_payment_with_pdq()
    if pdq_payment_confirmed:
        transaction_code, username, time_of_transaction, date_of_transaction = parse_transaction_details(message)
        print("Thank you for shopping with us.")
        insert_user_details_into_mysql(username, time_of_transaction, date_of_transaction, transaction_code)
    else:
        print("Payment confirmation failed. Please try again or contact support.")

# Function to process payment and store transaction details
@app.route('/process_payment', methods=['POST'])
def process_payment():
    if request.method == 'POST':
        message = request.form.get('message')
        process_pdq_transaction(message)
    return 'Payment processed successfully'

# Function to retrieve and display transactions
@app.route('/transactions')
def transactions():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT * FROM transactions''')
    transactions = c.fetchall()
    total_sales = sum(transaction[2] for transaction in transactions)
    conn.close()
    return render_template('transactions.html', transactions=transactions, total_sales=total_sales)

if __name__ == '__main__':
    create_sqlite_db()
    create_mysql_db()
    app.run(debug=True)
