import os
import json
import datetime
import mysql.connector

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS products
                          (id INT AUTO_INCREMENT PRIMARY KEY,
                           product_name VARCHAR(255),
                           description TEXT,
                           quantity INT,
                           actual_quantity INT,
                           return_quantity INT,
                           waste_quantity INT)''')
        conn.commit()
    except mysql.connector.Error as e:
        print("Error:", e)

def add_product(conn, product_info):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO products (product_name, description, quantity, actual_quantity, return_quantity, waste_quantity)
                          VALUES (%s, %s, %s, %s, %s, %s)''', (product_info['product_name'], product_info['description'],
                                                           product_info['quantity'], product_info['actual_quantity'],
                                                           product_info['return_quantity'], product_info['waste_quantity']))
        conn.commit()
        print("Product added successfully.")
    except mysql.connector.Error as e:
        print("Error:", e)

def main():
    try:
        # Establish a connection to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456",
            database="inventory"
        )
        create_table(conn)

        while True:
            print("1. Add Product")
            print("2. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                # Collect product information and add to the database
                while True:
                    try:
                        initial_quantity = int(input("Initial Quantity: "))
                        break  # Exit the loop if the input is a valid integer
                    except ValueError:
                        print("Invalid input. Please enter a valid integer.")

                product_info = {
                    "product_name": input("Product Name: "),
                    "description": input("Product Description: "),
                    "quantity": initial_quantity,  # Use the validated integer value
                    "actual_quantity": int(input("Actual Quantity: ")),
                    "return_quantity": 0,
                    "waste_quantity": 0
                }
                add_product(conn, product_info)

            elif choice == "2":
                print("Exiting the program.")
                break

            else:
                print("Invalid choice. Please select a valid option.")

    except mysql.connector.Error as e:
        print("Database error:", e)
    finally:
        if conn:
            conn.close()
# Product database
PRODUCT_DB_FILE = "../product_db.json"

def load_product_db():
    if os.path.exists(PRODUCT_DB_FILE):
        with open(PRODUCT_DB_FILE, "r") as file:
            return json.load(file)
    return {}

def save_product_db(product_db):
    with open(PRODUCT_DB_FILE, "w") as file:
        json.dump(product_db, file, indent=4)

def add_product(product_db, product_info):
    product_id = len(product_db) + 1
    product_info["id"] = product_id
    product_db[product_id] = product_info
    save_product_db(product_db)

def record_return(product_db, product_id, return_quantity):
    if product_id in product_db:
        product_db[product_id]["return_quantity"] += return_quantity
        save_product_db(product_db)

def record_waste(product_db, product_id, waste_quantity):
    if product_id in product_db:
        product_db[product_id]["waste_quantity"] += waste_quantity
        save_product_db(product_db)

def perform_physical_count(product_db, product_id, actual_quantity):
    if product_id in product_db:
        product_db[product_id]["actual_quantity"] = actual_quantity
        save_product_db(product_db)

def audit(product_db):
    audit_report = []
    for product_id, product_info in product_db.items():
        if product_info["actual_quantity"] < product_info["quantity"]:
            audit_report.append({
                "product_id": product_id,
                "discrepancy": product_info["quantity"] - product_info["actual_quantity"]
            })
    return audit_report

def backup_data():
    backup_dir = "backup"
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    backup_file = os.path.join(backup_dir, f"backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    with open(PRODUCT_DB_FILE, "r") as src_file, open(backup_file, "w") as dest_file:
        dest_file.write(src_file.read())

def restore_data(backup_file):
    if os.path.exists(backup_file):
        with open(backup_file, "r") as file:
            backup_data = json.load(file)
            save_product_db(backup_data)

if __name__ == "__main__":
    product_db = load_product_db()

    while True:
        print("Loss Prevention System Menu")
        print("1. Add Product")
        print("2. Record Return")
        print("3. Record Waste")
        print("4. Perform Physical Count")
        print("5. Audit")
        print("6. Backup Data")
        print("7. Restore Data")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            # Collect product information and add to the database
            while True:
                try:
                    initial_quantity = int(input("Initial Quantity: "))
                    break  # Exit the loop if the input is a valid integer
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

            product_info = {
                "product_name": input("Product Name: "),
                "description": input("Product Description: "),
                "quantity": initial_quantity,  # Use the validated integer value
                "actual_quantity": int(input("Actual Quantity: ")),
                "return_quantity": 0,
                "waste_quantity": 0
            }
            add_product(product_db, product_info)


        # ... Implement the other options (2-7) here

        elif choice == "8":
            print("Exiting the Loss Prevention System")
            break
