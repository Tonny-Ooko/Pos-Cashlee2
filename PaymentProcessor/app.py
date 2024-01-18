from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__, template_folder='.')

# MySQL database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'payment_transactions'

mysql = MySQL(app)


@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        data = request.get_json()
        customer_name = data['customer_name']
        payment_amount = data['payment_amount']
        payment_method = data['payment_method']
        transaction_notes = data['transaction_notes']

        cur = mysql.connection.cursor()
        insert_query = "INSERT INTO transactions (customer_name, amount, payment_method, transaction_notes, transaction_date) VALUES (%s, %s, %s, %s, %s)"
        transaction_date = datetime.now()
        values = (customer_name, payment_amount, payment_method, transaction_notes, transaction_date)
        cur.execute(insert_query, values)
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Payment processed successfully."}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
