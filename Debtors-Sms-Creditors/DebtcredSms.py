from tkinter import Entry, ttk, Button, scrolledtext
import mysql.connector
import tkinter as tk
import tk
from twilio.rest import Client
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "DebtcredSms"
}

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:123456@localhost/DebtcredSms"
db = SQLAlchemy(app)

# Twilio API configuration
twilio_account_sid = "your_account_sid"
twilio_auth_token = "your_auth_token"
twilio_phone_number = "your_twilio_phone_number"

twilio_client = Client(twilio_account_sid, twilio_auth_token)


class Debtors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    debtor_name = db.Column(db.String(100), nullable=False)
    debt_amount = db.Column(db.Float, nullable=False)
    identification_number = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


class Creditors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creditor_name = db.Column(db.String(100), nullable=False)
    credit_amount = db.Column(db.Float, nullable=False)
    identification_number = db.Column(db.String(20), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        debtor_name = request.form["debtor_name"]
        debt_amount = request.form["debt_amount"]
        identification_number = request.form["identification_number"]
        phone_number = request.form["phone_number"]
        debtors = Debtors(debtor_name=debtor_name, debt_amount=debt_amount,
                          identification_number=identification_number, phone_number=phone_number)
        db.session.add(debtors)
        db.session.commit()
    return render_template("index.html")

# Twilio API configuration
twilio_account_sid = "your_account_sid"
twilio_auth_token = "your_auth_token"
twilio_phone_number = "your_twilio_phone_number"

twilio_client = Client(twilio_account_sid, twilio_auth_token)

class EntryWithPlaceholder(Entry):
    def __init__(self, master=None, placeholder="", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        self.bind("<FocusIn>", self.clear_placeholder)
        self.bind("<FocusOut>", self.restore_placeholder)

    def clear_placeholder(self, event):
        if self.get() == self.placeholder:
            self.delete("0", "end")

    def restore_placeholder(self, event):
        if not self.get():
            self.insert("0", self.placeholder)


class DebtcredSmsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Debtors, Creditors, and SMS Marketing")

        self.create_ui()

    def create_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        debtors_tab = ttk.Frame(self.notebook)
        creditors_tab = ttk.Frame(self.notebook)
        sms_marketing_tab = ttk.Frame(self.notebook)

        self.notebook.add(debtors_tab, text="Debtors")
        self.notebook.add(creditors_tab, text="Creditors")
        self.notebook.add(sms_marketing_tab, text="SMS Marketing")

        self.create_debtors_ui(debtors_tab)
        self.create_creditors_ui(creditors_tab)
        self.create_sms_ui(sms_marketing_tab)

    def create_debtors_ui(self, tab):
        self.debtor_name_var = tk.StringVar()
        self.debtor_name_var.set("Debtor Name")
        EntryWithPlaceholder(tab, textvariable=self.debtor_name_var, placeholder="Debtor Name").pack()

        self.debt_amount_var = tk.StringVar()
        self.debt_amount_var.set("Debt Amount")
        EntryWithPlaceholder(tab, textvariable=self.debt_amount_var, placeholder="Debt Amount").pack()

        self.identification_number_var = tk.StringVar()
        self.identification_number_var.set("Identification Number")
        EntryWithPlaceholder(tab, textvariable=self.identification_number_var,
                             placeholder="Identification Number").pack()

        self.phone_number_var = tk.StringVar()
        self.phone_number_var.set("Phone Number")
        EntryWithPlaceholder(tab, textvariable=self.phone_number_var, placeholder="Phone Number").pack()

        Button(tab, text="Update Debtors", command=self.update_debtors).pack()
        Button(tab, text="Check Debts", command=self.check_debts).pack()

        self.debtors_message_box = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=40, height=10)
        self.debtors_message_box.pack()

    def create_creditors_ui(self, tab):
        self.creditor_name_var = tk.StringVar()
        self.creditor_name_var.set("Creditor Name")
        EntryWithPlaceholder(tab, textvariable=self.creditor_name_var, placeholder="Creditor Name").pack()

        self.credit_amount_var = tk.StringVar()
        self.credit_amount_var.set("Credit Amount")
        EntryWithPlaceholder(tab, textvariable=self.credit_amount_var, placeholder="Credit Amount").pack()

        self.identification_number_var = tk.StringVar()
        self.identification_number_var.set("Identification Number")
        EntryWithPlaceholder(tab, textvariable=self.identification_number_var,
                             placeholder="Identification Number").pack()

        self.phone_number_var = tk.StringVar()
        self.phone_number_var.set("Phone Number")
        EntryWithPlaceholder(tab, textvariable=self.phone_number_var, placeholder="Phone Number").pack()

        Button(tab, text="Update Creditors", command=self.update_creditors).pack()
        Button(tab, text="Check Creditors", command=self.check_creditors).pack()

        self.creditors_message_box = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=40, height=10)
        self.creditors_message_box.pack()

    def create_sms_ui(self, tab):
        self.sms_message_var = tk.StringVar()
        self.sms_message_var.set("SMS Message")
        EntryWithPlaceholder(tab, textvariable=self.sms_message_var, placeholder="SMS Message").pack()

        Button(tab, text="Write Message", command=self.write_sms).pack()
        Button(tab, text="Send SMS", command=self.send_sms).pack()

        self.sms_message_box = scrolledtext.ScrolledText(tab, wrap=tk.WORD, width=40, height=10)
        self.sms_message_box.pack()

    def update_debtors(self):
        debtor_name = self.debtor_name_var.get()
        debt_amount = self.debt_amount_var.get()


        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            insert_query = "INSERT INTO Debtors (debtor_name, debt_amount)VALUES (%s, %s,)"
            data = (debtor_name, debt_amount)
            cursor.execute(insert_query, data)
            conn.commit()
            self.debtors_message_box.insert(tk.END, "Debtor information updated.\n")
        except mysql.connector.Error as err:
            self.debtors_message_box.insert(tk.END, f"Error: {err}\n")
        finally:
            if conn:
                conn.close()

    def check_debts(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            select_query = "SELECT debtor_name, debt_amount, phone_number, identification_number FROM Debtors"
            cursor.execute(select_query)
            result = cursor.fetchall()
            for row in result:
                self.debtors_message_box.insert(tk.END, f"Debtor: {row[0]}, Debt: {row[1]}, Phone: {row[2]}, ID: {row[3]}\n")
        except mysql.connector.Error as err:
            self.debtors_message_box.insert(tk.END, f"Error: {err}\n")
        finally:
            if conn:
                conn.close()

    def update_debtors(self):
        debtor_name = self.debtor_name_var.get()
        debt_amount = self.debt_amount_var.get()
        identification_number = self.identification_number_var.get()
        phone_number = self.phone_number_var.get()  # Get the phone number value

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            insert_query = "INSERT INTO Debtors (debtor_name, debt_amount, identification_number, phone_number) VALUES (%s, %s, %s, %s)"
            data = (debtor_name, debt_amount, identification_number, phone_number)
            cursor.execute(insert_query, data)
            conn.commit()
            self.debtors_message_box.insert(tk.END, "Debtor information updated.\n")
        except mysql.connector.Error as err:
            self.debtors_message_box.insert(tk.END, f"Error: {err}\n")
        finally:
            if conn:
                conn.close()

    def update_creditors(self):
        creditor_name = self.creditor_name_var.get()
        credit_amount = self.credit_amount_var.get()
        identification_number = self.identification_number_var.get()
        phone_number = self.phone_number_var.get()  # Get the phone number value

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            insert_query = "INSERT INTO Creditors (creditor_name, credit_amount, identification_number, phone_number) VALUES (%s, %s, %s, %s)"
            data = (creditor_name, credit_amount, identification_number, phone_number)
            cursor.execute(insert_query, data)
            conn.commit()
            self.creditors_message_box.insert(tk.END, "Creditor information updated.\n")
        except mysql.connector.Error as err:
            self.creditors_message_box.insert(tk.END, f"Error: {err}\n")
        finally:
            if conn:
                conn.close()

    def check_creditors(self):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            select_query = "SELECT creditor_name, credit_amount, phone_number, identification_number FROM Creditors"
            cursor.execute(select_query)
            result = cursor.fetchall()
            for row in result:
                self.creditors_message_box.insert(tk.END,
                                                  f"Creditor: {row[0]}, Credit: {row[1]}, Phone: {row[2]}, ID: {row[3]}\n")
        except mysql.connector.Error as err:
            self.creditors_message_box.insert(tk.END, f"Error: {err}\n")
        finally:
            if conn:
                conn.close()

    def write_sms(self):
        sms_message = self.sms_message_var.get()
        self.sms_message_box.insert(tk.END, f"Message: {sms_message}\n")

    def send_sms(self):
        sms_message = self.sms_message_var.get()
        phone_numbers = []  # Retrieve phone numbers from your database

        try:
            for phone_number in phone_numbers:
                twilio_client.messages.create(
                    body=sms_message,
                    from_=twilio_phone_number,
                    to=phone_number
                )
                self.sms_message_box.insert(tk.END, f"SMS sent to {phone_number}: {sms_message}\n")
        except Exception as e:
            self.sms_message_box.insert(tk.END, f"Error sending SMS: {e}\n")



def main():
    root = tk.Tk()
    app = DebtcredSmsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
