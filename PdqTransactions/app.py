import datetime
import random
import mysql.connector
from flask import Flask

app = Flask(__name__, template_folder='.')


# Simulating PDQ payment confirmation (Replace this with actual PDQ API integration)
def confirm_payment_with_pdq():
    return random.choice([True, False])  # Simulating a random success or failure


# Function to parse the message and extract transaction details
def parse_transaction_details(message):
    # Assuming the message contains transaction code, username, time, and date
    # Replace the parsing logic below with the actual parsing based on your message format
    transaction_code = "123456"  # Replace with the actual parsed value
    username = "John Doe"  # Replace with the actual parsed value
    time_of_transaction = "12:34:56"  # Replace with the actual parsed value
    date_of_transaction = "2023-07-30"  # Replace with the actual parsed value
    return transaction_code, username, time_of_transaction, date_of_transaction


# Function to insert user details into the MySQL database
def insert_user_details_into_database(username, time_of_transaction, date_of_transaction, transaction_code):
    # Connect to the MySQL database (Replace 'your_host', 'your_username', 'your_password', and 'your_database' with your actual credentials)
    connection = mysql.connector.connect(
        host='localhost',
        user='rootexit',
        password='123456',
        database='point_of_sale'
    )
    cursor = connection.cursor()

    # Create the PointSale table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS PointSale (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL,
                        time_of_transaction VARCHAR(8) NOT NULL,
                        date_of_transaction DATE NOT NULL,
                        day VARCHAR(10) NOT NULL,
                        transaction_code VARCHAR(50) NOT NULL)''')

    # Get the current day of the week
    day_of_week = datetime.datetime.strptime(date_of_transaction, "%Y-%m-%d").strftime('%A')

    # Insert user details into the PointSale table
    insert_query = '''INSERT INTO PointSale (username, time_of_transaction, date_of_transaction, day, transaction_code)
                      VALUES (%s, %s, %s, %s, %s)'''
    insert_values = (username, time_of_transaction, date_of_transaction, day_of_week, transaction_code)
    cursor.execute(insert_query, insert_values)

    # Commit the changes and close the connection
    connection.commit()
    connection.close()


# Main function to process the transaction
def process_transaction(message):
    pdq_payment_confirmed = confirm_payment_with_pdq()

    if pdq_payment_confirmed:
        transaction_code, username, time_of_transaction, date_of_transaction = parse_transaction_details(message)
        print("Thank you for shopping with us.")
        insert_user_details_into_database(username, time_of_transaction, date_of_transaction, transaction_code)
    else:
        print("Payment confirmation failed. Please try again or contact support.")


# Replace this with actual PDQ integration to receive the message from the PDQ system
# For demonstration purposes, the message is hardcoded here.
# In a real-world scenario, this message would be received from the PDQ system.
pdq_message = "Transaction Code: 123456, Username: John Doe, Time: 12:34:56, Date: 2023-07-30"
process_transaction(pdq_message)
