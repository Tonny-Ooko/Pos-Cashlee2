from flask import Flask, render_template, request, redirect, url_for, session, flash, Response
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



# Create an instance of the PasswordHasher with custom configuration if needed
ph = PasswordHasher(
    time_cost=2,  # Adjust time cost as needed
    memory_cost=102400,  # Adjust memory cost as needed
    parallelism=8,  # Adjust parallelism as needed
)

# Initialize OAuth with your credentials

app = Flask(__name__, template_folder='.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://TONNY:123456@localhost/point_of_sale'
app.secret_key = '1234Tonny!Ooko'  # Replace with your secret key



# Initialize URLSafeSerializer instance
serializer = URLSafeSerializer(app.secret_key)

data = "1234Tonny!Ooko"

# Replace occurrences of url_quote with quote
encoded_string = quote(data)

# Replace occurrences of url_decode with unquote
decoded_string = unquote(encoded_string)


# Configuration for Google OAuth
client_id = '822402527612-jqbrumfeup205aabomol0hibeq73n4vi.apps.googleusercontent.com'
client_secret = 'GOCSPX-WQ7JECy4Hf0Q9lPIl9oSVYfoENV'
redirect_uri = 'your_redirect_uri'
scope = ['https://mail.google.com/']

# Google OAuth endpoints
authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
token_url = 'https://oauth2.googleapis.com/token'
authorize_url = 'https://accounts.google.com/o/oauth2/auth'




# Add the OAuth credentials to your Flask config
app.config['GOOGLE_CLIENT_ID'] = '822402527612-jqbrumfeup205aabomol0hibeq73n4vi.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = 'GOCSPX-WQ7JECy4Hf0Q9lPIl9oSVYfoENV'
app.config['GOOGLE_DISCOVERY_URL'] = 'https://accounts.google.com/.well-known/openid-configuration'

# Define a regular expression pattern for a strong password (e.g., at least one uppercase letter, one lowercase letter, one digit, and at least six characters long)
password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$')

app.config['SECRET_KEY'] = '1234Tonny!Ooko'  # Set your generated secret key here
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'otienotonny55@gmail.com'
app.config['MAIL_PASSWORD'] = '12230002tonnyO'




db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)
#db.create_all()


class AuditResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result_text = db.Column(db.String(128))


class PaymentTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Define 'id' as the primary key
    date = db.Column(db.Date)
    amount = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))  # Assuming 'product' table has an 'id' column
    # Define a relationship with the Product model if needed
    product = db.relationship('Product', backref='transactions')
    # Add other fields as needed


class StoreManagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    # Add other fields as needed


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)
    # Add other fields as needed


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
@app.route('/generate_report')
def generate_report():
    # Define start_date and end_date here (e.g., from user input or a specific range)
    start_date = 'your_start_date'
    end_date = 'your_end_date'

    # Retrieve data from PaymentTransaction, StoreManagement, and PointOfSale tables
    sales_data = db.session.query(PaymentTransaction.date, PaymentTransaction.amount,StoreManagement.name, point_of_sale.name, point_of_sale.price) \
        .join(StoreManagement, StoreManagement.id == PaymentTransaction.store_id) \
        .join(point_of_sale, point_of_sale.id == PaymentTransaction.pos_id) \
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
        return redirect(url_for('index'))

    session['google_token'] = (response['access_token'], '')
    user_info = google.get('userinfo')

    # Store or use user_info as needed, e.g., save user to your database

    return 'Logged in as: ' + user_info.data['email']


#@google.tokengetter
#def get_google_oauth_token():
    #return session.get('google_token')


@app.route('/oauth_callback')
def oauth_callback():
    response = google.authorized_response()

    if response is None or response.get('access_token') is None:
        flash('Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        ))
        return redirect(url_for('index'))


class point_of_sale(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)  # Add this line
    password_hash = db.Column(db.String(128), nullable=False)  # Change '_password' to 'password_hash'
    #password = db.Column(db.String(128), nullable=False)  # New column for password
    role = db.Column(db.String(255))
    reset_token = db.Column(db.String(255))
    reset_token_expiration = db.Column(db.DateTime)


def __init__(self, username, email, password_hash, role):
    self.username = username
    self.email = email
    self.password_hash = password_hash  # Update to 'password_hash'
    self.role = role


def generate_reset_token():
    token = secrets.token_urlsafe(32)  # Generate a random token
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    return token, expiration


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/product_info")
def product_info():
    # In a real scenario, get user roles from the authentication process
    user_roles = ["Admin", "Manager"]  # Example roles
    return render_template("product_info.html", user_roles=user_roles)



# Define the registration route
@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]  # Ensure a password is provided
    role = request.form["registerOption"]

    # Check if the password field is empty
    if not password:
        flash("Password is required.", "error")
        return redirect(url_for("index"))

    # Password strength validation
    if not password_pattern.match(password):
        flash(
            "Password must be at least six characters long and contain at least one uppercase letter, one lowercase letter, and one digit.",
            "error")
        return redirect(url_for("registration"))

    if not point_of_sale.query.filter_by(username=username).first():
        # User does not exist, create a new user
        # Hash the password using Argon2
        ph = PasswordHasher()
        hashed_password = ph.hash(password)  # Hash the password using Argon2

        # Print the hashed password
        print(f"Hashed Password: {hashed_password}")

        new_user = point_of_sale(username=username, email=email, password_hash=hashed_password,
                        role=role)  # Update 'password' to 'password_hash'
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")

        # Redirect to product_info page after successful registration
        return redirect(url_for('product_info'))

    else:
        flash("Username already exists", "error")

    # If registration is not successful, render the registration page again
    return render_template('registration.html')



@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # Verify the token and expiration time
    user = point_of_sale.query.filter_by(reset_token=token).first()
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
            return redirect(url_for("login"))
        return render_template("reset_password")
    else:
        flash("Invalid or expired token. Please request a new password reset.", "error")
        return redirect(url_for("reset_password"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = point_of_sale.query.filter_by(email=email).first()
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = point_of_sale.query.filter_by(username=username).first()
        print("User fetched from the database:", user)

        if user and argon2.verify(password, user.password_hash):
            # Valid credentials, set user session
            session["user_id"] = user.id
            return redirect(url_for("product_info"))  # Change to the appropriate page
        else:
            flash("Invalid username or password", "error")

    return render_template("index.html")

@app.route('/audit', methods=['GET', 'POST'])
def audit():
    # Assuming 'AuditResult' is a model representing audit results in your database

    if request.method == 'POST':
        result_text = request.form.get('result_text')
        audit_result = AuditResult(result_text=result_text)
        db.session.add(audit_result)
        db.session.commit()

    audit_results = AuditResult.query.all()
    return render_template('audit.html', audit_results=audit_results)

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("index"))


# Route for showing a success message after registration
@app.route("/registration_success")
def registration_success():
    return render_template("index.html", registration_successful=True)


# Route for showing a success message after password reset
@app.route("/password_reset_success")
def password_reset_success():
    return render_template("index.html", password_reset_successful=True)


if __name__ == "__main__":
    app.run(debug=True)
