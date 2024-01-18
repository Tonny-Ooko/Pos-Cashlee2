# Import the necessary modules and classes
from flask import (
    Flask, render_template, request, flash, redirect, url_for, session,
    send_file, jsonify, current_app,Blueprint
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, login_required, current_user, logout_user, UserMixin
)
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sqlalchemy.ext.hybrid import hybrid_property

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

# Import passlib and passlib-related classes
from passlib.hash import argon2, bcrypt_sha256, sha256_crypt
from passlib.context import CryptContext

# Import argon2-specific classes
from argon2 import PasswordHasher, exceptions as argon2_exceptions
from argon2.exceptions import VerifyMismatchError
# Import your custom modules
from .auth_module import db,User
from .your_auth_module import find_user  # Adjust this import as needed
from .custom_json_encoder import CustomJSONEncoder  # Import your custom JSON encoder
from flask_jwt_extended import create_access_token

app = Flask(__name__, template_folder='.')
#$app.json_encoder = CustomJSONEncoder  # Set the custom JSON encoder
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/users'
#db = SQLAlchemy(app)
db.init_app(app)
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
app.json_encoder = CustomJSONEncoder

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Replace these with your actual database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "users"
}

app.secret_key = "12230tonnyOoko^%$3"  # Change this to a secret key for session management


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

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email



@app.route('/api/data')
def get_data():
    data = {'key': 'value', 'number': 42}
    return jsonify(data)

@hybrid_property
def password(self):
        return self._password

def hash_password(password):
    return bcrypt_sha256.hash(password)

# Define a route that retrieves a user by username
@app.route('/user/<username>')
def get_user(username):
    user = find_user(username)
    if user:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404

@password.setter
def password(self, value):
        self._password = ph.hash(value)


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


@auth_bp.route('/login', methods=['GET'])
def display_login_form():
    # Render your login form template here
    return render_template('login.html')

def user_to_dict(user):
    return {
        'id': user.id,
        'username': user.username,
        'role': user.role
    }

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.is_json:
            try:
                data = request.get_json()
                username = data.get('username').strip()
                password = data.get('password').strip()
                role = data.get('role').strip()
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
                if ph.verify(user.password_hash, password):
                    if role == user.role:
                        db.session.commit()  # Commit the changes

                        # Store the user's ID in the session
                        session['user_id'] = username

                        print("Login successful.")  # Add a debug statement

                        # Redirect to the 'index' route when login is successful
                        return redirect(url_for('index'))
                    else:
                        return jsonify({'message': 'Login failed. Invalid role.'}), 401
                else:
                    return jsonify({'message': 'Login failed. Invalid credentials.'}), 401
            except argon2_exceptions.VerifyMismatchError:
                return jsonify({'message': 'Login failed. Invalid credentials.'}), 401
        else:
            print(f"User '{username}' not found in the database.")  # Add a debug statement
            return jsonify({'message': 'User not found.'}), 404

    # If it's a GET request, render the login page
    return render_template('login.html')

# Define the index routec
@app.route('/index')
def index():
    # Add logic here to ensure that only authenticated users can access 'index.html'
    if 'user_id' in session:
        username = session['user_id']
        return render_template('index.html', user={'username': username})
    else:
        return redirect(url_for('login'))  # Redirect to login if user is not authenticated

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
        return redirect(url_for('login'))

# Define the sales_report route
@app.route('/sales_report')
def sales_report():
    if 'user_id' in session:
        return render_template('sales_report.html')
    else:
        return redirect(url_for('login'))

# Define the top_selling_products_report route
@app.route('/top_selling_products_report')
def top_selling_products_report():
    if 'user_id' in session:
        return render_template('top_selling_products_report.html')
    else:
        return redirect(url_for('login'))

# Define the revenue_trends_report route
@app.route('/revenue_trends_report')
def revenue_trends_report():
    if 'user_id' in session:
        return render_template('revenue_trends_report.html')
    else:
        return redirect(url_for('login'))

@app.route('/')
def home():
    if 'user' in session:
        user = session['user']
        return render_template('index.html', user=user)
    else:
        return redirect(url_for('login'))


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
# Create similar routes and functions for other reports (e.g., top_selling_products_report_pdf, revenue_trends_report_pdf).

# Import the User model
from .auth_module import User  # Adjust the import path as needed
if __name__ == '__main__':
    app.run()

