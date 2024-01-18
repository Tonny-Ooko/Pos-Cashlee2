from flask import Flask, render_template, request, redirect, url_for, flash,send_file
import mysql.connector
import pdfkit
from datetime import datetime


app = Flask(__name__, template_folder='.')
app.secret_key = 'your_secret_key'

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "inventory"
}

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           product_name VARCHAR(255),
                           description TEXT,
                           quantity INT,
                           actual_quantity INT,
                           return_quantity INT,
                           waste_quantity INT)''')
        conn.commit()
    except mysql.connector.Error as e:
        print("Error:", e)

def add_product(conn, product_info):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO products (product_name, description, quantity, actual_quantity, return_quantity, waste_quantity)
                          VALUES (%s, %s, %s, %s, %s, %s)''', (product_info['product_name'], product_info['description'],
                                                           product_info['quantity'], product_info['actual_quantity'],
                                                           product_info['return_quantity'], product_info['waste_quantity']))
        conn.commit()
        flash("Product added successfully.", "success")
    except mysql.connector.Error as e:
        flash("Error adding product.", "error")
        print("Error:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        product_info = {
            "product_name": request.form['product_name'],
            "description": request.form['description'],
            "quantity": int(request.form['quantity']),
            "actual_quantity": int(request.form['actual_quantity']),
            "return_quantity": 0,
            "waste_quantity": 0
        }
        try:
            conn = mysql.connector.connect(**db_config)
            create_table(conn)
            add_product(conn, product_info)
            conn.close()
        except mysql.connector.Error as e:
            flash("Database error.", "error")
            print("Database error:", e)
    return render_template('add_product.html')

@app.route('/record_return', methods=['GET', 'POST'])
def record_return_route():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        return_quantity = int(request.form['return_quantity'])
        try:
            conn = mysql.connector.connect(**db_config)
            product_db = retrieve_product_db(conn)  # Pass the database connection (conn) as an argument
            record_return(conn, product_db, product_id, return_quantity)
            conn.close()
            flash("Return recorded successfully.", "success")
        except mysql.connector.Error as e:
            flash("Database error.", "error")
            print("Database error:", e)

    return render_template('record_return.html')
# Modify the retrieve_product_db function to accept a database connection as an argument
def retrieve_product_db(conn):
    try:
        cursor = conn.cursor()

        # Execute a query to retrieve product data from the database
        query = "SELECT * FROM your_product_table"  # Replace with your actual query
        cursor.execute(query)

        # Fetch the product data
        product_db = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return product_db
    except mysql.connector.Error as e:
        # Handle the database error
        print("Database error:", e)
        return None  # Return None to indicate an error


# Usage example
try:
    conn = mysql.connector.connect(**db_config)
    product_data = retrieve_product_db(conn)
    if product_data is not None:
        print("Product data:", product_data)
    else:
        print("Error retrieving product data.")
    conn.close()
except mysql.connector.Error as e:
    print("Database error:", e)

def record_return(conn, product_db, product_id, return_quantity):
    # Replace this with your actual record return logic
    # Example: Update the return_quantity field in the database
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET return_quantity = return_quantity + %s WHERE id = %s", (return_quantity, product_id))
    conn.commit()

# Define the record_waste function to update waste quantity
def record_waste(conn, product_db, product_id, waste_quantity):
    try:
        cursor = conn.cursor()

        # Update the waste_quantity for the specified product_id in the database
        update_query = "UPDATE products SET waste_quantity = waste_quantity + %s WHERE id = %s"
        cursor.execute(update_query, (waste_quantity, product_id))

        conn.commit()
    except mysql.connector.Error as e:
        flash("Database error.", "error")
        print("Database error:", e)
    finally:
        cursor.close()



# Route for recording waste
@app.route('/record_waste', methods=['GET', 'POST'])
def record_waste_route():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        waste_quantity = int(request.form['waste_quantity'])
        try:
            conn = mysql.connector.connect(**db_config)
            product_db = retrieve_product_db(conn)  # You need to implement retrieve_product_db
            record_waste(conn, product_db, product_id, waste_quantity)
            conn.close()
            flash("Waste recorded successfully.", "success")
        except mysql.connector.Error as e:
            flash("Database error.", "error")
            print("Database error:", e)

    # Fetch product data again after recording waste (you can optimize this)
    try:
        conn = mysql.connector.connect(**db_config)
        product_db = retrieve_product_db(conn)
        conn.close()
    except mysql.connector.Error as e:
        flash("Database error.", "error")
        print("Database error:", e)

    return render_template('record_waste.html', product_db=product_db)

@app.route('/perform_physical_count', methods=['GET', 'POST'])
def perform_physical_count_route():
    if request.method == 'POST':
        # Handle POST request data here
        product_name = request.form.get('product_name')
        product_id = request.form.get('product_id')
        actual_quantity = request.form.get('actual_quantity')

        # Generate HTML content for the PDF
        pdf_html = f"""
               <html>
               <head>
                   <title>Physical Count Report</title>
               </head>
               <body>
                   <h1>Physical Count Report</h1>
                   <p><strong>Product Name:</strong> {product_name}</p>
                   <p><strong>Product ID:</strong> {product_id}</p>
                   <p><strong>Actual Quantity:</strong> {actual_quantity}</p>
               </body>
               </html>
               """

        # Generate a PDF file from the HTML content
        pdfkit.from_string(pdf_html, 'physical_count_report.pdf',configuration=pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf'))
        # Optionally, you can redirect to another page or show a success message
        flash("Data recorded successfully.", "success")

        return send_file(
            'physical_count_report.pdf',
            as_attachment=True,
            download_name='physical_count_report.pdf',  # Use download_name instead
        )

    elif request.method == 'GET':
        try:
            conn = mysql.connector.connect(**db_config)
            # Retrieve the product_db data from the database or wherever it's stored
            product_db = retrieve_product_db(conn)  # Implement retrieve_product_db
            conn.close()
        except mysql.connector.Error as e:
            flash("Database error.", "error")
            print("Database error:", e)
            product_db = None  # Set product_db to None in case of an error

        if product_db is None:
            # Handle the case where product_db is None (e.g., show an error message)
            flash("Product data not available.", "error")

        # Render the template with the product_db data or None
        return render_template('perform_physical_count.html', product_db=product_db)

# Define the retrieve_sales_data function
def retrieve_sales_data(conn):
    # Your code to retrieve sales data from the database goes here
    # Make sure to return the sales data in an appropriate format
    pass

# Define the audit function
def audit(product_db, sales_db):
    # Calculate total sales
    total_sales = 0
    for sale in sales_db:
        total_sales += sale['quantity_sold'] * sale['unit_price']

    # Generate a sales report
    sales_report = []
    for sale in sales_db:
        product = next((product for product in product_db if product['id'] == sale['product_id']), None)
        if product:
            sales_report.append({
                'product_name': product['name'],
                'quantity_sold': sale['quantity_sold'],
                'total_revenue': sale['quantity_sold'] * sale['unit_price'],
                'sale_date': sale['sale_date'],
            })

    # Calculate the total number of products in the database
    total_products = len(product_db)

    # Create an audit report
    audit_report = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_sales': total_sales,
        'total_products': total_products,
        'sales_report': sales_report,
    }

    return audit_report

# Route for the audit page
@app.route('/audit')
def audit_route():
    try:
        conn = mysql.connector.connect(**db_config)
        product_db = retrieve_product_db(conn)  # Retrieve product data
        sales_db = retrieve_sales_data(conn)  # Retrieve sales data
        conn.close()
    except mysql.connector.Error as e:
        flash("Database error.", "error")
        print("Database error:", e)
        product_db = None
        sales_db = None

    if product_db is None or sales_db is None:
        flash("Data not available for audit.", "error")
        return redirect(url_for('index'))  # Redirect to the home page or an appropriate page

    audit_report = audit(product_db, sales_db)  # Generate the audit report

    return render_template('audit.html', audit_report=audit_report)

def backup_data():
    # Your code to back up data goes here
    pass

@app.route('/backup_data')
def backup_data_route():
    backup_data()
    flash("Data backed up successfully.", "success")
    return redirect(url_for('index'))

def restore_data(backup_file):
    # Your code to restore data from the backup file goes here
    pass

@app.route('/restore_data/<backup_file>')
def restore_data_route(backup_file):
    restore_data(backup_file)
    flash("Data restored successfully.", "success")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
