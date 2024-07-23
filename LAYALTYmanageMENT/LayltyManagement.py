import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, scrolledtext
import mysql.connector

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "point_of_sale"
}

class Customer:
    def __init__(self, phone_number):
        self.phone_number = phone_number
        self.points = 0

class PointOfSaleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sale and Loyalty Management")

        self.customers = {}

        self.create_ui()

    def create_ui(self):
        self.phone_number_var = StringVar()
        self.product_name_var = StringVar()
        self.product_price_var = StringVar()

        Label(self.root, text="Phone Number:").pack()
        Entry(self.root, textvariable=self.phone_number_var).pack()

        Label(self.root, text="Product Name:").pack()
        Entry(self.root, textvariable=self.product_name_var).pack()

        Label(self.root, text="Product Price:").pack()
        Entry(self.root, textvariable=self.product_price_var).pack()

        Button(self.root, text="Process Sale", command=self.process_sale).pack()

        self.message_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def process_sale(self):
        phone_number = self.phone_number_var.get()
        product_name = self.product_name_var.get()
        product_price = float(self.product_price_var.get())

        if phone_number not in self.customers:
            self.customers[phone_number] = Customer(phone_number)

        customer = self.customers[phone_number]
        points_earned = int(product_price // 100)

        # Update MySQL database
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert transaction data into the database
            insert_query = "INSERT INTO transactions (phone_number, product_name, product_price, points_earned) VALUES (%s, %s, %s, %s)"
            transaction_data = (customer.phone_number, product_name, product_price, points_earned)
            cursor.execute(insert_query, transaction_data)
            conn.commit()

            self.message_box.insert(tk.END, f"Sale processed for {customer.phone_number}.\n")
            self.message_box.insert(tk.END, f"Product: {product_name}, Price: {product_price}\n")
            self.message_box.insert(tk.END, f"Points Earned: {points_earned}\n")

            customer.points += points_earned
            self.message_box.insert(tk.END, f"Total Points: {customer.points}\n")

        except mysql.connector.Error as err:
            print("MySQL Error:", err)

        finally:
            if conn:
                conn.close()

def main():
    root = tk.Tk()
    app = PointOfSaleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
