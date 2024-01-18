from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='.')
app.secret_key = '123456TonnyOoko^'
# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "PointOfSale"
}

@app.route('/', methods=['GET', 'POST'])
def apply_promotion():
    if request.method == 'POST':
        product_name = request.form['product_name']
        discount_percentage_str = request.form['discount_percentage']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Get the current price of the product
            get_price_query = "SELECT price FROM Products WHERE name = %s"
            cursor.execute(get_price_query, (product_name,))
            result = cursor.fetchone()

            if result is not None:
                product_price = result[0]

                # Calculate the discounted price
                discount_percentage = float(discount_percentage_str.strip('%')) / 100
                discounted_price = product_price * (1 - discount_percentage)

                # Update the Products table with the new discount
                update_query = "UPDATE Products SET discount = %s WHERE name = %s"
                cursor.execute(update_query, (discount_percentage, product_name))
                conn.commit()

                flash(f"Promotion applied: {discount_percentage_str} discount on {product_name}.", "success")
                flash(f"Original Price: ${product_price:.2f}", "info")
                flash(f"Discounted Price: ${discounted_price:.2f}", "info")

                # Update the TransactionHistory table
                insert_transaction_query = "INSERT INTO TransactionHistory (product_name, original_price, discounted_price) VALUES (%s, %s, %s)"
                cursor.execute(insert_transaction_query, (product_name, product_price, discounted_price))
                conn.commit()
            else:
                flash(f"Error: Product '{product_name}' not found.", "error")

        except mysql.connector.Error as err:
            flash(f"Error: {err}", "error")

        finally:
            if conn:
                conn.close()

    return render_template('apply_promotion.html')

if __name__ == "__main__":
    app.secret_key = '123456TonnyOoko^'  # Set your secret key for session management
    app.run(debug=True)
