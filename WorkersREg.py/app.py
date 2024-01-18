from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, EqualTo, Regexp
import mysql.connector


app = Flask(__name__, template_folder='.')
app.secret_key = "Tonnyt%*^ooko12@2023"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'Products'



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[
        InputRequired(),
        Length(min=6, message="Password should be at least 6 characters long."),
        Regexp(r'^(?=.*[a-z])(?=.*[A-Z])',
               message="Password should have at least one uppercase and one lowercase character."),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Confirm Password')
    id_number = StringField('ID Number', validators=[InputRequired()])
    kra_number = StringField('KRA Number', validators=[InputRequired()])
    bank_account = StringField('Bank Account', validators=[InputRequired()])
    salary = StringField('Salary', validators=[InputRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[InputRequired()])
    duration_of_work = StringField('Duration of Work', validators=[InputRequired()])
    shift = StringField('Shift', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user_data = {
            'username': form.username.data,
            'password': form.password.data,
            'id_number': form.id_number.data,
            'kra_number': form.kra_number.data,
            'bank_account': form.bank_account.data,
            'salary': form.salary.data,
            'gender': form.gender.data,
            'duration_of_work': form.duration_of_work.data,
            'shift': form.shift.data
        }
        if save_user_to_db(user_data):
            print("User registered successfully.")
            flash("User registered successfully.", "success")
        else:
            print("Error while saving user to the database.")
            flash("Error while saving user to the database.", "error")
    return render_template('register.html', form=form)

def save_user_to_db(user_data):
    conn = None
    try:
        conn = mysql.connector.connect()
        if conn.is_connected():
            print("Connected to the database.")
        else:
            print("Failed to connect to the database.")

        cursor = conn.cursor()

        placeholders = ", ".join(["%s"] * len(user_data))
        columns = ", ".join(user_data.keys())
        values = tuple(user_data.values())

        insert_query = f"INSERT INTO employees ({columns}) VALUES ({placeholders})"
        print("Query:", insert_query)
        print("Values:", values)

        cursor.execute(insert_query, values)
        conn.commit()  # Commit the transaction

        flash("User registered successfully.", "success")
        return True

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        flash(f"Error: {err}", "error")
        return False

    finally:
        if conn:
            if conn.is_connected():
                conn.close()
                print("Connection closed.")
            else:
                print("Connection is not established.")
        else:
            print("Connection was never initiated.")

if __name__ == '__main__':
    app.run(debug=True)