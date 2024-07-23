import mysql.connector
from flask import Flask, render_template, request

# Create a Flask web application
app = Flask(__name__, template_folder='.')

# Configure MySQL connection
db_config = {
    "host": "localhost",
    "user": "TONNY",
    "password": "123456",
    "database": "Product"

}

class Product:
    def __init__(self, product_info, quantity_info, pricing_info, supplier_info):
        self.product_info = product_info
        self.quantity_info = quantity_info
        self.pricing_info = pricing_info
        self.supplier_info = supplier_info

    def save_to_db(self):
        conn = None
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insert product info
            cursor.execute("""
                 INSERT INTO Product 
                (name, description, sku, barcode, brand, category, unit, 
                current_stock, minimum_stock, maximum_stock, reorder_quantity, 
                stock_status, location, selling_price, cost_price, profit_margin, 
                special_discounts, supplier_name, supplier_contact, supplier_code, lead_time) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s)
            """, (
                request.form.get('productName'),
                request.form.get('productDescription'),
                request.form.get('productSku'),
                request.form.get('productBarcode'),
                request.form.get('productBrand'),
                request.form.get('productCategory'),
                request.form.get('productUnit'),
                request.form.get('productCurrentStock'),
                request.form.get('productMinimumStock'),
                request.form.get('productMaximumStock'),
                request.form.get('productReorderQuantity'),
                request.form.get('productStockStatus'),
                request.form.get('productLocation'),
                request.form.get('productSellingPrice'),
                request.form.get('productCostPrice'),
                request.form.get('productProfitMargin'),
                request.form.get('productSpecialDiscounts'),
                request.form.get('productSupplierName'),
                request.form.get('productSupplierContact'),
                request.form.get('productSupplierCode'),
                request.form.get('productLeadTime')
            ))

            conn.commit()
            return True  # Product saved successfully

        except mysql.connector.Error as err:
            print("Database Error:", err)
            return False  # Product registration failed

        finally:
            if conn:
                conn.close()

@app.route('/', methods=['GET', 'POST'])
def product_registration():
    if request.method == 'POST':
        # Handle form submission and database insertion here
        product_data = {
            "product_info": {
                "name": request.form.get('productName'),
                "description": request.form.get('productDescription'),
                "sku": request.form.get('productSku'),
                "barcode": request.form.get('productBarcode'),
                "brand": request.form.get('productBrand'),
                "category": request.form.get('productCategory'),
                "unit": request.form.get('productUnit')
            },
            "quantity_info": {
                "current_stock": request.form.get('productCurrentStock'),  # Corrected field name
                "minimum_stock": request.form.get('productMinimumStock'),
                "maximum_stock": request.form.get('productMaximumStock'),
                "reorder_quantity": request.form.get('productReorderQuantity'),
                "stock_status": request.form.get('productStockStatus'),
                "location": request.form.get('productLocation')
            },
            "pricing_info": {
                "selling_price": request.form.get('productSellingPrice'),
                "cost_price": request.form.get('productCostPrice'),
                "profit_margin": request.form.get('productProfitMargin'),
                "special_discounts": request.form.get('productSpecialDiscounts')
            },
            "supplier_info": {
                "supplier_name": request.form.get('productSupplierName'),
                "supplier_contact": request.form.get('productSupplierContact'),
                "supplier_code": request.form.get('productSupplierCode'),
                "lead_time": request.form.get('productLeadTime')
            }
        }

        product = Product(**product_data)
        if product.save_to_db():
            message = "Product registered successfully!"
        else:
            message = "Error: Product registration failed."

        return render_template('inventory.html', message=message)

    return render_template('inventory.html', message=None)

if __name__ == "__main__":
    app.run(debug=True, port=40000)  # Change 8080 to your desired port number

