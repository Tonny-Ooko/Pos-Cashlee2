from flask import (
    Flask, render_template, request, flash, redirect, url_for, session,
    send_file, jsonify, current_app,Blueprint, Response)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required, current_user, logout_user, UserMixin)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.ext.hybrid import hybrid_property
from requests.auth import HTTPBasicAuth
from flask_migrate import Migrate
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import mysql.connector
from datetime import datetime, timedelta
import hashlib
import logging
import os
import sys

# Import passlib and passlib-related classes
from passlib.hash import argon2, bcrypt_sha256, sha256_crypt
from passlib.context import CryptContext

# Import argon2-specific classes
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from argon2.exceptions import VerifyMismatchError
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length
import mysql.connector
from flask_mysqldb import MySQL
from flask_cors import CORS
import pdfkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_dance.contrib.google import make_google_blueprint, google
import secrets
import google
from itsdangerous import URLSafeSerializer
import datetime
from flask_migrate import Migrate
import re  # Import the re module for regular expressions
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from argon2 import PasswordHasher  # Import these for URL manipulation
from passlib.hash import argon2
from werkzeug.urls import quote, unquote
import requests
from requests.auth import HTTPBasicAuth



# Create an instance of the PasswordHasher with custom configuration if needed
ph = PasswordHasher(
    time_cost=2,  # Adjust time cost as needed
    memory_cost=102400,  # Adjust memory cost as needed
    parallelism=8,  # Adjust parallelism as needed
)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

template_dir = resource_path('templates')
print(f'Template directory: {template_dir}')

app = Flask(__name__, template_folder=template_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://TONNY:123456@localhost/point_of_sale'
#db = SQLAlchemy(app)
migrate = Migrate(app)
Base = declarative_base()
login_manager = LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)
login_manager.login_view = 'auth.display_login_form'
Base = declarative_base()
auth_bp = Blueprint('auth', __name__)
# Create an instance of the PasswordHasher with custom configuration if needed
ph = PasswordHasher()
# Initialize the passlib context
pwd_context = CryptContext(schemes=["argon2"])
# Set the custom JSON encoder
db = SQLAlchemy(app)
# Configure logging

logging.basicConfig(level=logging.DEBUG)
headers = {"Content-Type": "application/json"}
app.secret_key = "Tonnyt%*^ooko12@2023"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'TONNY'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'point_of_sale'
CORS(app)  # Enable CORS for all routes


# Initialize URLSafeSerializer instance
serializer = URLSafeSerializer(app.secret_key)

data = "Tonnyt%*^ooko12@2023"

# Replace occurrences of url_quote with quote
encoded_string = quote(data)

# Replace occurrences of url_decode with unquote
decoded_string = unquote(encoded_string)'

# Define a regular expression pattern for a strong password (e.g., at least one uppercase letter, one lowercase letter, one digit, and at least six characters long)
password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$')

app.config['SECRET_KEY'] = '1234Tonny!Ooko'  # Set your generated secret key here
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'otienotonny55@gmail.com'
app.config['MAIL_PASSWORD'] = '12230002tonnyO'


# Establish a database connection
conn = mysql.connector.connect(
    host='localhost',
    user='TONNY',
    password='123456',
    database='point_of_sale'
)


mysql = MySQL(app)
mail = Mail(app)
migrate = Migrate(app, db)
cursor = conn.cursor()


db_config = {
    "host": "localhost",
    "user": "TONNY",
    "password": "123456",
    "database": " Product"
}


# Function to get access token
def get_access_token(consumer_key, consumer_secret):
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to obtain access token: {response.status_code} - {response.text}")

@app.route('/register_urls', methods=['POST'])
def register_urls():
    try:
       
        if response.status_code == 200:
            return jsonify({'message': 'URLs registered successfully'}), 200
        else:
            print(f"Failed to register URLs: {response.status_code} - {response.text}")
            return jsonify({'error': 'Failed to register URLs', 'details': response.json()}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/confirmation', methods=['POST'])
def handle_confirmation():
    data = request.json
    print("Received confirmation notification:", data)
    return jsonify({'message': 'Confirmation notification received'}), 200

@app.route('/validation', methods=['POST'])
def handle_validation():
    data = request.json
    print("Received validation notification:", data)
    return jsonify({'message': 'Validation notification received'}), 200

@app.route('/')
def loading_screen():
    return render_template('loading_screen.html')


def register_product(barcode, name, selling_price):
    try:
        cursor.execute('''INSERT INTO Product (barcode, name, selling_price)
                          VALUES (%s, %s, %s)''', (barcode, name, selling_price))
        conn.commit()
        print("Product registered successfully!")
    except mysql.connector.IntegrityError:
        print("Product with the same barcode already exists!")


# Function to fetch product information by barcode with input validation and sanitization
def fetch_product(barcode):
    cursor.execute('''SELECT * FROM Product WHERE barcode=%s''', (barcode,))
    product = cursor.fetchone()
    if product:
        print("Product found:")
        print("Barcode:", product[0])
        print("Name:", product[1])
        print("selling_price:", product[2])
    else:
        print("Product not found.")


# Route to handle product registration form submission with input validation
@app.route('/register_D', methods=['POST'])
def register_D():
    barcode = request.form['barcode']
    name = request.form['name']
    price = request.form['selling_price']

    # Input validation
    if not barcode or not name or not price:
        return "Invalid input. Please fill in all fields."

    # Sanitization
    barcode = barcode.strip()
    name = name.strip()
    price = price.strip()

    # Register product
    register_product(barcode, name, price)
    return "Product registered successfully!"


# Route to handle product retrieval form submission with input validation
@app.route('/fetch', methods=['POST'])
def fetch():
    barcode = request.form['barcode']

    # Input validation
    if not barcode:
        return "Invalid input. Please provide a barcode."

    # Sanitization
    barcode = barcode.strip()

    # Fetch product
    fetch_product(barcode)
    return "Product fetched successfully!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
         Check login credentials here
         If login is successful, redirect to HomePage.html
        # Example:
        if login_successful:
            return redirect(url_for('home_page'))
        return redirect(url_for('home_page'))  

    return render_template('login.html')


@app.route('/HomePage.html')
def home_page():
    return render_template('HomePage.html', notification=request.args.get('notification'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Your registration logic goes here
    return render_template('register.html')


class User(db.Model):
    __tablename__ = 'user_info'  # Match the actual table name in your database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Add this line
    reset_token = db.Column(db.String(255))
    reset_token_expiration = db.Column(db.DateTime)


Base = declarative_base()


def __json__(self):
    return {
        'id': self.id,
        'username': self.username,
        'role': self.role
    }


def create_app():
    # Other app setup code (e.g., blueprints, JWT, etc.) goes here
    return app

def some_function():
    db = current_app.db

def __init__(self, username):
        self.username = username

@app.route('/api/data')
def get_data():
    data = {'key': 'value', 'number': 42}
    return jsonify(data)


def hash_password(password):
    return bcrypt_sha256.hash(password)

# Define a route that retrieves a user by username


@app.route('/protected')
@jwt_required
def protected_route():
    current_user_id = get_jwt_identity()
    user = load_user(current_user_id)
    return jsonify({'message': 'This route is protected', 'user': user.__json__()}), 200

@staticmethod
def check_password(entered_password, stored_password_hash):
    try:
        print(f"Stored Password Hash: {stored_password_hash}")
        print(f"Entered Password: {entered_password}")
        ph.verify(stored_password_hash, entered_password)
        return True
    except argon2_exceptions.VerifyMismatchError:
        return False


@auth_bp.route('/login1', methods=['GET'])
def display_login_form():
    # Render your login form templates here
    return render_template('login1.html')

def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'role': user.role
    }



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    id_number = StringField('ID Number', validators=[InputRequired()])
    kra_number = StringField('KRA Number', validators=[InputRequired()])
    bank_account = StringField('Bank Account', validators=[InputRequired()])
    salary = StringField('Salary', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    duration_of_work = StringField('Duration of Work', validators=[InputRequired()])
    shift = StringField('Shift', validators=[InputRequired()])
    phone_number = StringField('Phone Number', validators=[InputRequired(), Length(max=10)])
    role = StringField('Role', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        id_number = request.form['id_number']
        kra_number = request.form['kra_number']
        bank_account = request.form['bank_account']
        salary = request.form['salary']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        duration_of_work = request.form['duration_of_work']
        shift = request.form['shift']
        role = request.form['role']

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert registration details into the database
        cur.execute(
            "INSERT INTO employees (username, id_number, kra_number, bank_account, salary, gender, phone_number, duration_of_work, shift, role) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (username, id_number, kra_number, bank_account, salary, gender, phone_number, duration_of_work, shift, role))

        # Commit to database
        mysql.connection.commit()

        # Close cursor
        cur.close()

        # Set success message
        success_message = 'Registration successful!'
    else:
        success_message = None

    return render_template('homepage.html', success_message=success_message)



@app.route('/check_workers', methods=['GET'])
def check_workers():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employees")
        workers = cur.fetchall()
        cur.close()
        return render_template('check_workers.html', workers=workers)
    except Exception as e:
        flash("Error retrieving workers from the database.", "error")
        return render_template('check_workers.html')


# Route to handle deletion of workers by their ID
@app.route('/delete_worker/<int:worker_id>', methods=['GET', 'POST'])
def delete_worker(worker_id):
    try:
        # Execute SQL DELETE statement to remove the worker with the specified ID
        cursor.execute("DELETE FROM employees WHERE id = %s", (worker_id,))

        # Commit the transaction to apply the changes
        conn.commit()

        # Close the database connection (assuming conn and cursor are defined globally)
        cursor.close()

        # Flash a success message
        flash(f'Deleted worker with ID {worker_id} successfully.', 'success')

        # Redirect the user to the check_workers page after deletion
        return redirect('/check_workers')

    except Exception as e:
        # Handle any errors that occur during deletion
        flash(f'Error deleting worker with ID {worker_id}: {e}', 'error')
        return redirect('/check_workers')  # Redirect back to check_workers page


def authenticate(username, password, role):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Strip leading and trailing whitespace from the entered username and role
        username = username.strip()
        role = role.strip()

        query = "SELECT username, password_hash, role FROM user_info WHERE username = %s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()

        if user_data:
            username_db, stored_password_hash, stored_role = user_data

            # Verify the entered password against the stored Argon2 hash
            try:
                if argon2.verify(password, stored_password_hash):
                    print("Password is correct.")
                    if role == stored_role:
                        print(f"Role successful.")
                        print(f"User '{username}' successfully authenticated.")
                        return User(username=username_db, role=role)
                    else:
                        print(f"Invalid role. Role not found in the database.")
                else:
                    print("Password is incorrect.")
            except VerifyMismatchError:
                print("Password verification failed.")
        else:
            print(f"User '{username}' not found in the database.")

        return None
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        return None
    finally:
        if conn:
            conn.close()

# Define the login route
@app.route('/login1', methods=['GET', 'POST'])
def login1():
    if request.method == 'POST':
        if request.is_json:
            try:
                data = request.get_json()
                username = data.get('username')
                password = data.get('password')
                role = data.get('role')
            except Exception as e:
                print(f"Error parsing JSON data: {str(e)}")
                return jsonify({'message': 'Invalid JSON data.'}), 400
        else:
            # If the request is not JSON, try to parse it as form data
            username = request.form.get('username')
            password = request.form.get('password')
            role = request.form.get('role')

        # Check if any of the required fields are missing
        if not username or not password or not role:
            return jsonify({'message': 'Invalid request. Required fields missing.'}), 400

        # Query the database to check if the user exists
        user = User.query.filter_by(username=username).first()
        if user:
            # Verify the password hash
            try:
                if user and argon2.verify(password, user.password_hash):
                    if role == user.role:
                        session['username'] = user.username  # Store the user's ID in the session
                        print("Login successful.")  # Add a debug statement

                        # Redirect to the 'index' route when login is successful
                        return redirect(url_for('index'))
                    else:
                        return jsonify({'message': 'Login failed. Invalid role.'}), 401
                else:
                    return jsonify({'message': 'Login failed. Invalid credentials.'}), 401
            except Exception as e:
                print(f"Error verifying password: {str(e)}")
                return jsonify({'message': 'Login failed. Internal server error.'}), 500
        else:
            print(f"User '{username}' not found in the database.")  # Add a debug statement
            return jsonify({'message': 'User not found.'}), 404

    # If it's a GET request or login fails, render the login page
    return render_template('login1.html')

@app.route('/index')
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index1.html', username=username)
    else:
        return redirect(url_for('login_page'))



# Register the blueprint with your app
app.register_blueprint(auth_bp, url_prefix='/auth')

# Define a protected route that requires authentication
@app.route('/protected', methods=['GET'], endpoint='protected_route')
@jwt_required
def protected_route():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'message': 'This route is protected', 'user': user}), 200


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()  # This logs out the user using Flask-Login
    session.pop('user_id', None)  # Remove the user_id from the session
    flash("Logged out successfully.", "success")

    if request.is_json:
        # If the request accepts JSON response, return JSON
        return jsonify({'message': 'Logout successful'}), 200
    else:
        # Otherwise, redirect to the login page
        return redirect(url_for('login1'))

# Define the sales_report route
@app.route('/sales_report')
def sales_report():
    if 'user_id' in session:
        return render_template('sales_report.html')
    else:
        return redirect(url_for('login1'))

# Define the top_selling_products_report route
@app.route('/top_selling_products_report')
def top_selling_products_report():
    if 'user_id' in session:
        return render_template('top_selling_products_report.html')
    else:
        return redirect(url_for('login1'))

# Define the revenue_trends_report route
@app.route('/revenue_trends_report')
def revenue_trends_report():
    if 'user_id' in session:
        return render_template('revenue_trends_report.html')
    else:
        return redirect(url_for('login1'))

@app.route('/')
def home():
    if 'user' in session:
        user = session['user']
        return render_template('index1.html', user=user)
    else:
        return redirect(url_for('login1'))


@app.route('/generate_sales_report_pdf', methods=['POST'])
def generate_sales_report_pdf():
    if 'user' in session:
        # Replace this with your actual database query to fetch sales data
        sales_data = [
            {"product_name": "Product 1", "total_sold": 100, "total_sales": 1000},
            {"product_name": "Product 2", "total_sold": 200, "total_sales": 2000},
            # Add more data as needed
        ]
        # You can return the PDF as a response
# report_module.py
def create_report(template, data, title):
    # Replace this with your actual report generation logic using libraries like PDFKit, WeasyPrint, or ReportLab.
    # This is a simple placeholder example.
    pdf_data = f"Generating a PDF report for {title} using data: {data}"
    return pdf_data

# your_data_module.py
def get_sales_data():
    # Replace this with your actual data retrieval logic, e.g., querying a database or reading from a file.
    sales_data = [
        {"product": "Product A", "sales": 100},
        {"product": "Product B", "sales": 200},
        # Add more data here
    ]
    return sales_data


@login_manager.user_loader
def load_user(user_id):
    # This function is required by Flask-Login to load a user by their ID.
    return User.get(user_id)  # You may need to adjust this based on your data structure.



@app.route('/generate_report', methods=['GET'])
@login_required
def generate_report():
    # Assuming 'sales_data' is defined somewhere in your code
    # Add your report generation logic here
    return 'This is the report generation page.'
    sales_data = get_sales_data()

    # Create a PDF report
    pdf = create_report('sales_report_pdf.html', data=sales_data, title='Sales Report')

    # Save the PDF to a temporary file and serve it using Flask's send_file
    pdf_filename = 'sales_report.pdf'
    pdf_path = '/path/to/your/pdf/directory/'  # Replace with the actual path
    pdf.save(os.path.join(pdf_path, pdf_filename))

    return send_file(os.path.join(pdf_path, pdf_filename), as_attachment=True, download_name=pdf_filename)

@app.route('/apply_promotion', methods=['GET', 'POST'])
def apply_promotion():
    if request.method == 'POST':
        product_name = request.form['product_name']
        discount_percentage_str = request.form['discount_percentage']

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Get the current price of the product
            get_price_query = "SELECT price FROM Product WHERE name = %s"
            cursor.execute(get_price_query, (product_name,))
            result = cursor.fetchone()

            if result is not None:
                product_price = result[0]

                # Calculate the discounted price
                discount_percentage = float(discount_percentage_str.strip('%')) / 100
                discounted_price = product_price * (1 - discount_percentage)

                # Update the Products table with the new discount
                update_query = "UPDATE Product SET discount = %s WHERE name = %s"
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

@app.route('/index1')
def home1():
    return render_template('index1.html')



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
            #create_table(conn)
            #add_product(conn, product_info)
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
        query = "SELECT * FROM Product"  # Replace with your actual query
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

        # Render the templates with the product_db data or None
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
import mysql.connector


@app.route('/audit')
def audit():
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
        return redirect(url_for('product_info'))  # Redirect to the home page or an appropriate page

    audit_report = audit(product_db, sales_db)  # Generate the audit report

    return render_template('audit.html', audit_report=audit_report)

def backup_data():
    # Your code to back up data goes here
    pass

@app.route('/backup_data')
def backup_data_route():
    backup_data()
    flash("Data backed up successfully.", "success")
    return redirect(url_for('index1'))

def restore_data(backup_file):
    # Your code to restore data from the backup file goes here
    pass

@app.route('/restore_data/<backup_file>')
def restore_data_route(backup_file):
    restore_data(backup_file)
    flash("Data restored successfully.", "success")
    return redirect(url_for('index1'))

@app.route('/product_entry')
def product_entry():
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

        return redirect(url_for('product_entry'))

@app.route('/index2', methods=['GET', 'POST'])
def index2():
    message = None  # Initialize message variable
    if request.method == 'POST':
        if 'check_debtors' in request.form:
            # Fetch debtors from the database and display in table
            cursor.execute("SELECT * FROM debtors")
            debtors = cursor.fetchall()
            return render_template('index1.html', debtors=debtors)  # Render index1.html with debtor details
        else:
            debtor_name = request.form['debtor_name']
            debt_amount = request.form['debt_amount']
            identification_number = request.form['identification_number']
            phone_number = request.form['phone_number']

            # Insert or update user details in the database
            query = "INSERT INTO debtors (debtor_name, debt_amount, identification_number, phone_number) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE debt_amount=%s, identification_number=%s, phone_number=%s"
            cursor.execute(query, (debtor_name, debt_amount, identification_number, phone_number, debt_amount, identification_number, phone_number))
            db.commit()
            message = 'Details updated successfully!'  # Update message variable
    return render_template('index2.html', message=message)


@app.route('/creditors')
def creditors():
    # Fetch creditor data from your database
    creditors_data = [
        {"creditor_name": "Creditor A", "credit_amount": 1000, "identification_number": "123",
         "phone_number": "123-456-7890"},
        {"creditor_name": "Creditor B", "credit_amount": 1500, "identification_number": "456",
         "phone_number": "987-654-3210"},
        # Add more creditors as needed
    ]

    return render_template('creditors.html', creditors=creditors_data)

import  requests


def send_sms(message, numbers):
    api_key = 'AC9e9974f6964d042b09de1dd6341293e4'  # Twilio Account SID
    auth_token = 'cb72e67a0d4d21885d098da2dd5e3d86'  # Twilio Auth Token
    base_url = f'https://api.twilio.com/2010-04-01/Accounts/{api_key}/Messages'

    success_count = 0  # Define success_count here

    for number in numbers:
        payload = {
            'From': '+16592645795',  # Your Twilio phone number
            'To': number,
            'Body': message
        }
        try:
            response = requests.post(base_url, data=payload, auth=(api_key, auth_token))
            if response.status_code == 201:
                success_count += 1
            else:
                print(f"Failed to send SMS to {number}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending SMS to {number}: {e}")

    print(f"Total success count: {success_count}")  # Print the total success count
    return success_count

@app.route('/sms', methods=['GET', 'POST'])
def sms():
    if request.method == 'POST':
        if 'send_sms' in request.form:
            message = request.form['message']
            phone_numbers = request.form['phone_numbers'].split(',')
            success_count = 0
            for number in phone_numbers:
                success = send_sms(message, number)  # Change here to capture success result
                if success:
                    success_count += 1
            return f"{success_count} SMS messages sent successfully!"  # Placeholder response
        elif 'search_numbers' in request.form:
            search_term = request.form['search_term']
            cursor.execute("SELECT * FROM phone_numbers WHERE phone_number LIKE %s", ("%" + search_term + "%",))
            phone_numbers = cursor.fetchall()
            return render_template('sms.html', phone_numbers=phone_numbers)
    return render_template('sms.html', phone_numbers=None)

@app.route('/email_marketing', methods=['GET', 'POST'])
def email_marketing():
    if request.method == 'POST':
        if 'send_email' in request.form:
            subject = request.form['subject']
            message = request.form['message']
            email_list = request.form['email_list'].split(',')

            sender_email = "otienotonny55@gmail.com"  # Replace with your email
            password = "sjhj bngi zxbt uxrw"  # Replace with your password

            for email in email_list:
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = email.strip()
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, password)
                    server.sendmail(sender_email, email.strip(), msg.as_string())

            return jsonify({'success': True, 'message': 'Email sent successfully!'})

    return render_template('email_marketing.html')


@app.route('/creditors2', methods=['GET', 'POST'])
def creditors2():
    message = None  # Initialize message variable
    if request.method == 'POST':
        if 'update_creditors' in request.form:
            creditor_name = request.form['creditor_name']
            credit_amount = request.form['credit_amount']
            identification_number = request.form['identification_number']
            phone_number = request.form['phone_number']

            # Code to update creditor details in the database
            query = "INSERT INTO Creditors (creditor_name, credit_amount, identification_number, phone_number) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (creditor_name, credit_amount, identification_number, phone_number))
            db.commit()

            message = "Creditor details updated successfully!"

        elif 'check_creditors' in request.form:
            # Code to retrieve creditor details from the database
            cursor.execute("SELECT * FROM Creditors")
            creditors = cursor.fetchall()
            return render_template('creditors.html', creditors=creditors)

    return render_template('creditors.html', message=message)

class Product:
    def __init__(self, product_info, quantity_info, pricing_info, supplier_info):
        self.product_info = product_info
        self.quantity_info = quantity_info
        self.pricing_info = pricing_info
        self.supplier_info = supplier_info

    def save_to_db(self):
        conn = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert product info
            cursor.execute("""
                 INSERT INTO Product 
                (name, description, sku, barcode, brand, category, unit, 
                current_stock, minimum_stock, maximum_stock, reorder_quantity, 
                stock_status, location, selling_price, cost_price, profit_margin, 
                special_discounts, supplier_name, supplier_contact, supplier_code, lead_time) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s)
            """, (
                request.form.get('productName'),
                request.form.get('productDescription'),
                request.form.get('productSku'),
                request.form.get('productBarcode'),
                request.form.get('productBrand'),
                request.form.get('productCategory'),
                request.form.get('productUnit'),
                request.form.get('productCurrentStock'),
                request.form.get('productMinimumStock'),
                request.form.get('productMaximumStock'),
                request.form.get('productReorderQuantity'),
                request.form.get('productStockStatus'),
                request.form.get('productLocation'),
                request.form.get('productSellingPrice'),
                request.form.get('productCostPrice'),
                request.form.get('productProfitMargin'),
                request.form.get('productSpecialDiscounts'),
                request.form.get('productSupplierName'),
                request.form.get('productSupplierContact'),
                request.form.get('productSupplierCode'),
                request.form.get('productLeadTime')
            ))

            conn.commit()
            return True  # Product saved successfully

        except mysql.connector.Error as err:
            print("Database Error:", err)
            return False  # Product registration failed

        finally:
            if conn:
                conn.close()

@app.route('/product_registration', methods=['GET', 'POST'])
def product_registration():
    if request.method == 'POST':
        # Handle form submission and database insertion here
        product_data = {
            "product_info": {
                "name": request.form.get('productName'),
                "description": request.form.get('productDescription'),
                "sku": request.form.get('productSku'),
                "barcode": request.form.get('productBarcode'),
                "brand": request.form.get('productBrand'),
                "category": request.form.get('productCategory'),
                "unit": request.form.get('productUnit')
            },
            "quantity_info": {
                "current_stock": request.form.get('productCurrentStock'),  # Corrected field name
                "minimum_stock": request.form.get('productMinimumStock'),
                "maximum_stock": request.form.get('productMaximumStock'),
                "reorder_quantity": request.form.get('productReorderQuantity'),
                "stock_status": request.form.get('productStockStatus'),
                "location": request.form.get('productLocation')
            },
            "pricing_info": {
                "selling_price": request.form.get('productSellingPrice'),
                "cost_price": request.form.get('productCostPrice'),
                "profit_margin": request.form.get('productProfitMargin'),
                "special_discounts": request.form.get('productSpecialDiscounts')
            },
            "supplier_info": {
                "supplier_name": request.form.get('productSupplierName'),
                "supplier_contact": request.form.get('productSupplierContact'),
                "supplier_code": request.form.get('productSupplierCode'),
                "lead_time": request.form.get('productLeadTime')
            }
        }

        product = Product(**product_data)
        if product.save_to_db():
            message = "Product registered successfully!"
        else:
            message = "Error: Product registration failed."

        return render_template('inventory.html', message=message)

    return render_template('inventory.html', message=None)


# Route to generate a sales report
@app.route('/generate_report45')
def generate_report45():
    # Retrieve the start_date and end_date query parameters from the URL
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Perform report generation using the provided dates
    # Update this logic based on your requirements

    return "Sales report generated for dates: {} to {}".format(start_date, end_date)


# Route to analyze profitability
@app.route('/analyze_profitability01')
def analyze_profitability01():
    # Retrieve the start_date and end_date query parameters from the URL
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Perform profitability analysis using the provided dates
    # Update this logic based on your requirements

    return "Profitability analysis for dates: {} to {}".format(start_date, end_date)


# Route to display product information page
@app.route('/product_information')
def product_information():
    # Retrieve and prepare product information to display on the page
    # Replace the following with your actual data retrieval logic
    product_info = [
        {'name': 'Product 1', 'description': 'Description 1', 'price': 10.99},
        {'name': 'Product 2', 'description': 'Description 2', 'price': 19.99},
        # Add more product data as needed
    ]

    return render_template('product_information.html', product_info=product_info)


# Route to generate a sales report
@app.route('/generate_report2')
def generate_report2():
    # Define start_date and end_date here (e.g., from user input or a specific range)
    start_date = 'your_start_date'
    end_date = 'your_end_date'

    # Retrieve data from PaymentTransaction, StoreManagement, and PointOfSale tables
    sales_data = db.session.query(PaymentTransaction.date, PaymentTransaction.amount,StoreManagement.name, User.name, User.price) \
        .join(StoreManagement, StoreManagement.id == PaymentTransaction.store_id) \
        .join(User, User.id == PaymentTransaction.pos_id) \
        .filter(PaymentTransaction.date >= start_date, PaymentTransaction.date <= end_date) \
        .all()
    # Create a Pandas DataFrame from the query result
    df = pd.DataFrame(sales_data, columns=['Date', 'Amount', 'Store', 'name ', ' price'])

    # Generate sales report (you can customize the report as needed)
    sales_report = df.groupby(['Store', 'Date']).agg({'Amount': 'sum'}).reset_index()

    # Create a plot (e.g., a bar chart) for the sales report
    plt.figure(figsize=(10, 6))
    for store, data in sales_report.groupby('Store'):
        plt.bar(data['Date'], data['Amount'], label=store)
    plt.xlabel('Date')
    plt.ylabel('Sales Amount')
    plt.title('Sales Report')
    plt.legend()

    # Save the plot to a BytesIO object
    plot_io = BytesIO()
    plt.savefig(plot_io, format='png')
    plot_io.seek(0)

    # Return the sales report as a downloadable PDF with the plot
    return Response(render_template('product_info.html', sales_report=sales_report),
                    headers={'Content-Type': 'application/pdf'})


# Route to analyze profitability
@app.route('/analyze_profitability')
def analyze_profitability():
    # Define start_date and end_date here (e.g., from user input or a specific range)
    start_date = 'your_start_date'
    end_date = 'your_end_date'

    # Retrieve data from Product and PaymentTransaction tables
    profitability_data = db.session.query(Product.name, Product.price, PaymentTransaction.amount) \
        .join(PaymentTransaction, Product.id == PaymentTransaction.product_id) \
        .filter(PaymentTransaction.date >= start_date, PaymentTransaction.date <= end_date) \
        .all()
    # Create a Pandas DataFrame from the query result
    df = pd.DataFrame(profitability_data, columns=['Product Name', 'Price', 'Amount'])

    # Calculate profit for each product
    df['Profit'] = df['Amount'] - (df['Price'] * df['Amount'])

    # Generate profitability analysis (you can customize the analysis as needed)
    profitability_analysis = df.groupby('Product Name').agg({'Amount': 'sum', 'Profit': 'sum'}).reset_index()

    # Return the profitability analysis as a downloadable PDF
    return Response(render_template('product_info.html', profitability_analysis=profitability_analysis),
                    headers={'Content-Type': 'application/pdf'})


@app.route('/login4')
def login4():
    return google.authorize(callback=url_for('oauth_callback', _external=True))


@app.route('/login/authorized')
def authorized():
    response = google.authorized_response()
    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={}, error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index3'))

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')

    # Store or use user_info as needed, e.g., save user to your database

    return 'Logged in as: ' + user_info.data['email']


@app.route('/oauth_callback')
def oauth_callback():
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index3'))





def __init__(self, username, email, password_hash, role):
    self.username = username
    self.email = email
    self.password_hash = password_hash  # Update to 'password_hash'
    self.role = role


def generate_reset_token():
    token = secrets.token_urlsafe(32)  # Generate a random token
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    return token, expiration


@app.route("/index3")
def index3():
    return render_template("index3.html")


@app.route("/product_info")
def product_info():
    # In a real scenario, get user roles from the authentication process
    user_roles = ["Admin", "Manager"]  # Example roles
    return render_template("product_info.html", user_roles=user_roles)



# Define the registration route
@app.route('/registration2')
def registration2():
    return render_template('registration2.html')


@app.route("/register2", methods=["GET", "POST"])
def register2():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]  # Ensure a password is provided
    role = request.form["registerOption"]

    # Check if the password field is empty
    if not password:
        flash("Password is required.", "error")
        return redirect(url_for("index3"))

    # Password strength validation
    if not password_pattern.match(password):
        flash(
            "Password must be at least six characters long and contain at least one uppercase letter, one lowercase letter, and one digit.",
            "error")
        return redirect(url_for("registration2"))

    if not User.query.filter_by(username=username).first():
        # User does not exist, create a new user
        # Hash the password using Argon2
        ph = PasswordHasher()
        hashed_password = ph.hash(password)  # Hash the password using Argon2

        # Print the hashed password
        print(f"Hashed Password: {hashed_password}")

        new_user = User(username=username, email=email, password_hash=hashed_password,
                        role=role)  # Update 'password' to 'password_hash'
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")

        # Redirect to product_info page after successful registration
        return redirect(url_for('product_info'))

    else:
        flash("Username already exists", "error")

    # If registration is not successful, render the registration page again
    return render_template('registration2.html')



@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # Verify the token and expiration time
    user = User.query.filter_by(reset_token=token).first()
    if user and user.reset_token_expiration > datetime.datetime.utcnow():
        if request.method == "POST":
            new_password = request.form.get("new_password")

            # Hash the new password using Argon2
            hashed_password = ph.hash(new_password)

            user.password_hash = hashed_password  # Update 'password' to 'password_hash'
            user.reset_token = None  # Clear the reset token
            user.reset_token_expiration = None
            db.session.commit()
            flash("Password reset successfully.", "success")
            return redirect(url_for("login4"))
        return render_template("reset_password")
    else:
        flash("Invalid or expired token. Please request a new password reset.", "error")
        return redirect(url_for("reset_password"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a random token and set the expiration time
            token = secrets.token_urlsafe(32)
            expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            user.reset_token = token
            user.reset_token_expiration = expiration
            db.session.commit()

            # Send the password reset email with the token
            msg = Message('Password Reset', recipients=[email])
            msg.body = f'Click the link below to reset your password:\n{url_for("reset_password", token=token, _external=True)}'
            mail.send(msg)

            flash("Password reset instructions sent to your email.", "success")
        else:
            flash("Email address not found.", "error")
    return render_template("forgot_password.html")

@app.route("/login2", methods=["GET", "POST"])
def login2():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        print("User fetched from the database:", user)

        if user and argon2.verify(password, user.password_hash):
            # Valid credentials, set user session
            session["user_id"] = user.id
            return redirect(url_for("product_info"))  # Change to the appropriate page
        else:
            flash("Invalid username or password", "error")

    return render_template("index3.html")

@app.route('/audit30', methods=['GET', 'POST'])
def audit30():
    # Assuming 'AuditResult' is a model representing audit results in your database

    if request.method == 'POST':
        result_text = request.form.get('result_text')
        audit_result = AuditResult(result_text=result_text)
        db.session.add(audit_result)
        db.session.commit()

    audit_results = AuditResult.query.all()
    return render_template('audit30.html', audit_results=audit_results)

@app.route("/logout2")
def logout2():
    session.pop("user_id", None)
    return redirect(url_for("index3"))


# Route for showing a success message after registration
@app.route("/registration_success")
def registration_success():
    return render_template("index3.html", registration_successful=True)


# Route for showing a success message after password reset
@app.route("/password_reset_success")
def password_reset_success():
    return render_template("index3.html", password_reset_successful=True)


@app.route('/recept', methods=['GET', 'POST'])
def recept():
    if request.method == 'POST':
        barcode = request.form['barcode']
        product = find_product(barcode)
        if product:
            name, price = product
            quantity = 1
            if similar_items(name, barcode):
                price *= 2  # Double the price for similar items
                quantity = 2
            return render_template('recept.html', name=name, price=price, quantity=quantity)
        else:
            return render_template('recept.html', error="Product not found")
    return render_template('recept.html')

def find_product(barcode):
    #conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT name, price FROM products WHERE barcode = ?''', (barcode,))
    product = c.fetchone()
    conn.close()
    return product

def similar_items(name, barcode):
    #conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''SELECT name FROM products WHERE name = ? AND barcode != ?''', (name, barcode))
    similar_item = c.fetchone()
    conn.close()
    return similar_item is not None

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
