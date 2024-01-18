from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector
import tkinter as tk
from tkinter import Label, Entry, Button, StringVar, scrolledtext

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "PointOfSale"
}

class PromotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Point of Sale Promotion")

        self.create_ui()

    def create_ui(self):
        self.product_name_var = StringVar()
        self.discount_percentage_var = StringVar()

        Label(self.root, text="Product Name:").pack()
        Entry(self.root, textvariable=self.product_name_var).pack()

        Label(self.root, text="Discount Percentage:").pack()
        Entry(self.root, textvariable=self.discount_percentage_var).pack()

        Button(self.root, text="Apply Promotion", command=self.apply_promotion).pack()

        self.message_box = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.message_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def apply_promotion(self):
        product_name = self.product_name_var.get()
        discount_percentage_str = self.discount_percentage_var.get()

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Get the current price of the product
            get_price_query = "SELECT price FROM Products WHERE name = %s"
            cursor.execute(get_price_query, (product_name,))
            result = cursor.fetchone()

            if result is not None:
                product_price = result[0]

                # Calculate the discounted price
                discount_percentage = float(discount_percentage_str.strip('%')) / 100
                discounted_price = product_price * (1 - discount_percentage)

                # Update the Products table with the new discount
                update_query = "UPDATE Products SET discount = %s WHERE name = %s"
                cursor.execute(update_query, (discount_percentage, product_name))
                conn.commit()

                self.message_box.insert(tk.END,
                                        f"Promotion applied: {discount_percentage_str} discount on {product_name}.\n")
                self.message_box.insert(tk.END, f"Original Price: ${product_price:.2f}\n")
                self.message_box.insert(tk.END, f"Discounted Price: ${discounted_price:.2f}\n\n")

                # Update the TransactionHistory table
                insert_transaction_query = "INSERT INTO TransactionHistory (product_name, original_price, discounted_price) VALUES (%s, %s, %s)"
                cursor.execute(insert_transaction_query, (product_name, product_price, discounted_price))
                conn.commit()
            else:
                self.message_box.insert(tk.END, f"Error: Product '{product_name}' not found.\n\n")

        except mysql.connector.Error as err:
            self.message_box.insert(tk.END, f"Error: {err}\n\n")

        finally:
            if conn:
                conn.close()


def main():
    root = tk.Tk()
    app = PromotionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
