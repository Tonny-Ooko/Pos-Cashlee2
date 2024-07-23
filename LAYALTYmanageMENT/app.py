from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__, template_folder='.')
app.secret_key = 'your_secret_key'

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "TONNY",
    "password": "123456",
    "database": "point_of_sale"
}

# Database Connection
conn = mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('product_entry.html')

@app.route('/process_sale', methods=['POST'])
def process_sale():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        product_name = request.form.get('product_name')
        product_price = float(request.form.get('product_price'))

        cursor = conn.cursor()

        # Create Customer if not exists
        cursor.execute("SELECT id, points FROM transactions WHERE phone_number = %s", (phone_number,))
        customer_data = cursor.fetchone()

        if customer_data is None:
            cursor.execute("INSERT INTO transactions (phone_number, points) VALUES (%s, 0)", (phone_number,))
            conn.commit()
            customer_id = cursor.lastrowid
            customer_points = 0
        else:
            customer_id, customer_points = customer_data

        # Calculate Points Earned
        points_earned = int(product_price // 100)
        customer_points += points_earned

        # Update Customer Points
        cursor.execute("UPDATE customers SET points = %s WHERE id = %s", (customer_points, customer_id))
        conn.commit()

        # Insert Transaction Data
        cursor.execute("INSERT INTO transactions (customer_id, product_name, product_price, points_earned) VALUES (%s, %s, %s, %s)",
                       (customer_id, product_name, product_price, points_earned))
        conn.commit()

        flash(f"Sale processed for {phone_number}.")
        flash(f"Product: {product_name}, Price: {product_price}")
        flash(f"Points Earned: {points_earned}")
        flash(f"Total Points: {customer_points}")

        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
