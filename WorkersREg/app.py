from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, Length
import mysql.connector
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__, template_folder='templates')
app.secret_key = "Tonnyt%*^ooko12@2023"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'TONNY'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'point_of_sale'
CORS(app)  # Enable CORS for all routes


# Establish a database connection
conn = mysql.connector.connect(
    host='localhost',
    user='TONNY',
    password='123456',
    database='point_of_sale'
)

mysql = MySQL(app)
cursor = conn.cursor()



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
def register():
    success_message = None
    if request.method == 'POST':
        # Get form data
        username = request.form['username']
        id_number = request.form['id_number']
        kra_number = request.form['kra_number']
        bank_account = request.form['bank_account']
        salary = request.form['salary']
        gender = request.form['gender']
        phone_number = request.form['phone_number']  # Added phone number field
        duration_of_work = request.form['duration_of_work']
        shift = request.form['shift']
        role = request.form['role']


        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query to insert registration details into the database
        cur.execute(
            "INSERT INTO employees (username, id_number, kra_number, bank_account, salary, gender,phone_number, duration_of_work, shift, role) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)",
            (username, id_number, kra_number, bank_account, salary, gender,phone_number , duration_of_work, shift, role))

        # Commit to database
        mysql.connection.commit()

        # Close connection
        cur.close()

        # Close connection
        cur.close()

        # Update success_message
        success_message = "User registered successfully."


    return render_template('register.html', success_message=success_message)


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

if __name__ == '__main__':
    app.run(debug=True, port=5001)