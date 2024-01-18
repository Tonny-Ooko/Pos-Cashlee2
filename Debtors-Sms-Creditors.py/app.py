from flask import Flask, render_template

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/creditors')
def creditors():
    # Fetch creditor data from your database
    creditors = [
        {"creditor_name": "Creditor A", "credit_amount": 1000, "identification_number": "123",
         "phone_number": "123-456-7890"},
        {"creditor_name": "Creditor B", "credit_amount": 1500, "identification_number": "456",
         "phone_number": "987-654-3210"},
        # Add more creditors as needed
    ]

    return render_template('creditors.html', creditors=creditors_data)

@app.route('/sms')
def sms():
    return render_template('sms.html')

if __name__ == '__main__':
    app.run(debug=True)
