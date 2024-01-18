from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
import tkinter as tk
from tkinter import messagebox

app = Flask(__name__)
# Configure MySQL connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "Products"
}

class Product:
    # ... (previous class methods and attributes)

    # Add methods for User Access and Security
    def set_user_roles(self, roles):
        self.user_roles = roles

    def authenticate_user(self, username, password):
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "SELECT * FROM Users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            user_data = cursor.fetchone()

            if user_data:
                self.user_roles = user_data[2]
                return True
            else:
                return False

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            if conn:
                conn.close()

class ProductApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Product Management")
        self.product = None

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Username:").pack()
        tk.Entry(self.root, textvariable=self.username_var).pack()

        tk.Label(self.root, text="Password:").pack()
        tk.Entry(self.root, textvariable=self.password_var, show="*").pack()

        tk.Button(self.root, text="Login", command=self.login).pack()

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        self.product = Product()
        if self.product.authenticate_user(username, password):
            self.show_product_ui()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def show_product_ui(self):
        product_ui = tk.Toplevel(self.root)
        product_ui.title("Product Information")

        # Get the user roles from the authenticated product instance
        user_roles = self.product.user_roles

        product_ui.wm_attributes("-topmost", 1)
        product_ui.focus_force()

        self.root.withdraw()  # Hide the login window

        # Render the template and pass user_roles as context
        product_ui.protocol("WM_DELETE_WINDOW", self.on_close)
        product_ui.protocol("WM_CLOSE", self.on_close)

        product_ui.wm_attributes("-topmost", 1)
        product_ui.focus_force()

        # Render the template and pass user_roles as context
        render_template("product_info.html", user_roles=user_roles)
        # Create and configure UI elements for product information
        # ... (you can add labels, entry fields, buttons, etc.)

        if "Admin" in self.product.user_roles:
            # Show admin-specific UI elements
            admin_button = tk.Button(product_ui, text="Generate Sales Report", command=self.product.generate_sales_report)
            admin_button.pack()

        if "Manager" in self.product.user_roles:
            # Show manager-specific UI elements
            manager_button = tk.Button(product_ui, text="Analyze Profitability", command=self.product.analyze_profitability)
            manager_button.pack()

        # ... (other UI elements)

def main():
    root = tk.Tk()
    app = ProductApp(root)
    root.mainloop()

if __name__ == "__main__":
        main()
