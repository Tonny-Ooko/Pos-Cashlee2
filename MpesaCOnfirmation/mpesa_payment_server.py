import re
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__, template_folder='.')

# Function to scan M-Pesa message for transaction code
def scan_mpesa_message(message):
    transaction_code_pattern = r'\b\d{10}\b'  # Assuming transaction code is a 10-digit number
    transaction_code = re.search(transaction_code_pattern, message)
    if transaction_code:
        return transaction_code.group()
    else:
        return None

# Function to check if a transaction code is successful (assuming you have a 'Transactions' table)
def check_transaction_success(transaction_code):
    # Replace this function with your implementation to check the transaction status
    # You can use the MySQL database or any other method to verify the transaction code
    return True

# Function to store transaction details in the MySQL database
def store_transaction_details(user_name, transaction_code, day, date, time):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='your_database'
        )
        cursor = conn.cursor()

        # Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS Ooko
                          (UserName VARCHAR(255), TransactionCode VARCHAR(50), Day VARCHAR(10), Date DATE, Time VARCHAR(8))''')

        # Insert the data into the table
        insert_query = "INSERT INTO Ooko (UserName, TransactionCode, Day, Date, Time) VALUES (%s, %s, %s, %s, %s)"
        insert_values = (user_name, transaction_code, day, date, time)
        cursor.execute(insert_query, insert_values)

        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print("Error while storing transaction details:", err)
        return False

@app.route('/mpesa_payment', methods=['POST'])
def mpesa_payment_webhook():
    data = request.get_json()

    # Extract the relevant details from the received data
    message = data.get('message')
    till_number = data.get('till_number')
    paybill_number = data.get('paybill_number')
    account_number = data.get('account_number')

    # Check if the message is related to the registered Till, Paybill, and Account numbers
    if scan_mpesa_message(message) and (till_number == 'your_registered_till_number' or
                                        paybill_number == 'your_registered_paybill_number' and
                                        account_number == 'your_registered_account_number'):
        # Assuming you have a way to get the user name, day, date, and time
        user_name = "John Doe"  # Replace this with your logic to get the user name
        day = "Monday"  # Replace this with your logic to get the day
        date = "2023-07-30"  # Replace this with your logic to get the date
        time = "12:34:56"  # Replace this with your logic to get the time

        # Store the transaction details
        store_transaction_details(user_name, scan_mpesa_message(message), day, date, time)

        # Assuming you have a way to verify the transaction status
        successful_payment = check_transaction_success(scan_mpesa_message(message))

        # Return a response to acknowledge the payment
        return jsonify({'status': 'success', 'message': 'Payment received and processed.'}), 200
    else:
        # Return a response to indicate the payment is not relevant to the registered numbers
        return jsonify({'status': 'success', 'message': 'Payment received but not relevant to registered numbers.'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
