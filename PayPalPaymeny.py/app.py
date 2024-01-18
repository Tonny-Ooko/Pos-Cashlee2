import mysql.connector
from flask import Flask, request
import paypalrestsdk

# Configure PayPal settings
from PaymentProcessor.PaymentTransaction import db_config

app = Flask(__name__, template_folder='.')


# Configure PayPal client
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": "your_client_id",
    "client_secret": "your_secret_key"
})

@app.route("/paypal_webhook", methods=["POST"])
def paypal_webhook():
    # Handle PayPal IPN data here
    payment_data = request.form.to_dict()
    # Process and store payment data in your database

    return "IPN received and processed"

def insert_payment(payer_name, amount, payment_date):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    insert_query = "INSERT INTO payments (payer_name, amount, payment_date) VALUES (%s, %s, %s)"
    data = (payer_name, amount, payment_date)
    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)