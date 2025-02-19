from flask import Flask, render_template, request, jsonify
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder='.')
# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="TONNY",  # Replace with your MySQL username
    password="123456",  # Replace with your MySQL password
    database="point_of_sale"
)
cursor = db.cursor()


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
    return render_template('index1.html', message=message)


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
    api_key = 'AFGHGJNNMKL<:>?>?:""""???>MLOGB JKKJN K M?KL JHN HN >KJN JLK'  # Twilio Account SID
    auth_token = 'WZREXFCRGVHBJNL:MFVGHJK NL>>K>OIKJHMVCFG HIUJXFCVHJB'  # Twilio Auth Token
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

            sender_email = "ghguvyhybhbhubk@gmail.com"  # Replace with your email
            password = "VBHNJOLI<JFKLYGBNUGIYV YBHUHH"  # Replace with your password

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



if __name__ == '__main__':
    app.run(debug=True)
