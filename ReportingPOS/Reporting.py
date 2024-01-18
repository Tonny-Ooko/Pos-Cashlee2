import mysql.connector
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Database connection configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "123456",
    "database": "PointOfSale"
}
class User:
    def __init__(self, username, password, role):
        self.username = username
        self.password = password
        self.role = role


def authenticate(username, password):
    # Authenticate the user by checking their credentials against the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = "SELECT username, role FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return User(username=user_data[0], password=password, role=user_data[1])
    else:
        return None


def main():
    print("Welcome to the Reporting System")

    # Authenticate the user
    username = input("Username: ")
    password = input("Password: ")
    user = authenticate(username, password)

    if user is None:
        print("Invalid credentials. Access denied.")
        return

    if user.role not in ["admin", "manager"]:
        print("Access denied. You don't have permission to use this system.")
        return

    print("Access granted. Welcome,", user.username)
class ReportingSystem:
    def __init__(self):
        self.db_config = {
            "host": "localhost",
            "user": "root",
            "password": "123456",
            "database": "PointOfSale"
        }
        self.connection = None

    def connect_to_database(self):
        self.connection = mysql.connector.connect(**self.db_config)

    def disconnect_from_database(self):
        if self.connection:
            self.connection.close()

    def generate_sales_report(self, start_date, end_date):
        self.connect_to_database()
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT product_name, SUM(quantity) AS total_sold, SUM(total_amount) AS total_sales
                FROM sales
                WHERE sale_date BETWEEN %s AND %s
                GROUP BY product_name
                ORDER BY total_sales DESC
            """
            cursor.execute(query, (start_date, end_date))
            sales_data = cursor.fetchall()

            # Process and display sales report
            self.display_sales_report(sales_data)

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            self.disconnect_from_database()

    def generate_top_selling_products_report(self, limit=10):
        self.connect_to_database()
        try:
            cursor = self.connection.cursor(dictionary=True)

            query = """
                SELECT product_name, SUM(quantity) AS total_sold
                FROM sales
                GROUP BY product_name
                ORDER BY total_sold DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            top_selling_data = cursor.fetchall()

            # Process and display top selling products report
            self.display_top_selling_products_report(top_selling_data)

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            self.disconnect_from_database()

    def display_sales_report(self, sales_data):
        print("Sales Report:")
        for row in sales_data:
            print(f"Product: {row['product_name']}")
            print(f"Total Sold: {row['total_sold']}")
            print(f"Total Sales: ${row['total_sales']:.2f}")
            print("=" * 30)

    def display_top_selling_products_report(self, top_selling_data):
        print("Top Selling Products Report:")
        for row in top_selling_data:
            print(f"Product: {row['product_name']}")
            print(f"Total Sold: {row['total_sold']}")
            print("=" * 30)

    def generate_revenue_trends_report(self, num_days):
        self.connect_to_database()
        try:
            cursor = self.connection.cursor(dictionary=True)

            end_date = datetime.now()
            start_date = end_date - timedelta(days=num_days)

            query = """
                SELECT sale_date, SUM(total_amount) AS daily_revenue
                FROM sales
                WHERE sale_date BETWEEN %s AND %s
                GROUP BY sale_date
                ORDER BY sale_date
            """
            cursor.execute(query, (start_date, end_date))
            revenue_data = cursor.fetchall()

            # Process and display revenue trends report
            self.display_revenue_trends_report(revenue_data)

        except mysql.connector.Error as err:
            print("Error:", err)

        finally:
            self.disconnect_from_database()

    def display_revenue_trends_report(self, revenue_data):
        dates = []
        revenues = []
        for row in revenue_data:
            dates.append(row['sale_date'].strftime("%Y-%m-%d"))
            revenues.append(row['daily_revenue'])

        plt.figure(figsize=(10, 6))
        plt.plot(dates, revenues, marker='o')
        plt.title("Revenue Trends")
        plt.xlabel("Date")
        plt.ylabel("Daily Revenue ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def main():
    reporting_system = ReportingSystem()

    while True:
        print("Reporting System Menu:")
        print("1. Generate Sales Report")
        print("2. Generate Top Selling Products Report")
        print("3. Generate Revenue Trends Report")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            reporting_system.generate_sales_report(start_date, end_date)

        elif choice == "2":
            limit = int(input("Enter number of top products to display: "))
            reporting_system.generate_top_selling_products_report(limit)

        elif choice == "3":
            num_days = int(input("Enter number of days for revenue trends: "))
            reporting_system.generate_revenue_trends_report(num_days)

        elif choice == "4":
            print("Exiting Reporting System.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
