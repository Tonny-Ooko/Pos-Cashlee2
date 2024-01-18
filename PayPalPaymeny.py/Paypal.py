import imaplib
import email
import re
import mysql.connector
# Import Flask and other necessary libraries
from flask import Flask, render_template, request, redirect, url_for

# Create a Flask app
app = Flask(__name__, template_folder='.')

# Define routes and views for your application
@app.route("/")
def index():
    # Implement your homepage view here
    return render_template("index.html")

# Add more routes as needed
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",
    "database": "paypal"
}

def insert_payment(payer_name, amount, payment_date):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        insert_query = "INSERT INTO payments (payer_name, amount, payment_date) VALUES (%s, %s, %s)"
        data = (payer_name, amount, payment_date)
        cursor.execute(insert_query, data)
        conn.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if conn:
            conn.close()
# Your PayPal email and password
paypal_email = "your_paypal_email@example.com"
paypal_password = "your_paypal_password"

# Connect to the PayPal email account using IMAP
imap_server = "imap.paypal.com"
imap_port = 993
imap = imaplib.IMAP4_SSL(imap_server, imap_port)
imap.login(paypal_email, paypal_password)

# Select the inbox folder
inbox_folder = "inbox"
imap.select(inbox_folder)

# Search for emails containing PayPal payment information
search_criteria = 'FROM "service@paypal.com" SUBJECT "Payment Received"'
status, email_ids = imap.search(None, search_criteria)

if status == "OK":
    email_ids = email_ids[0].split()
    for email_id in email_ids:
        # Fetch the email message
        status, msg_data = imap.fetch(email_id, "(RFC822)")
        if status == "OK":
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Extract payment details from the email content
            email_subject = email_message["subject"]
            email_body = email_message.get_payload(decode=True).decode("utf-8")

            # Parse the email body for payment details
            match = re.search(r"Received (\$\d+\.\d{2}) USD from (\w+).*?on (\d{4}-\d{2}-\d{2})", email_body, re.DOTALL)
            if match:
                amount_paid = match.group(1)
                payer_username = match.group(2)
                payment_date = match.group(3)

                # Log the payment details
                print(f"Payment Received:")
                print(f"Amount: {amount_paid}")
                print(f"Payer: {payer_username}")
                print(f"Payment Date: {payment_date}")
                print("\n")

# Logout and close the connection
imap.logout()
