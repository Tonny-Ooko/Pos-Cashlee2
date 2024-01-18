from django.shortcuts import render
from .models import Products  # Update the import statement to use the correct model


def product_registration(request):
    message = None
    if request.method == 'POST':
        product = Products(  # Use lowercase 'product' instead of 'Product'
            name=request.POST.get('productName'),
            description=request.POST.get('productDescription'),
            sku=request.POST.get('productSku'),
            barcode=request.POST.get('productBarcode'),
            brand=request.POST.get('productBrand'),
            category=request.POST.get('productCategory'),
            unit=request.POST.get('productUnit'),
            current_stock=request.POST.get('productCurrentStock'),
            minimum_stock=request.POST.get('productMinimumStock'),
            maximum_stock=request.POST.get('productMaximumStock'),
            reorder_quantity=request.POST.get('productReorderQuantity'),
            stock_status=request.POST.get('productStockStatus'),
            location=request.POST.get('productLocation'),
            selling_price=request.POST.get('productSellingPrice'),
            cost_price=request.POST.get('productCostPrice'),
            profit_margin=request.POST.get('productProfitMargin'),
            special_discounts=request.POST.get('productSpecialDiscounts'),
            supplier_name=request.POST.get('productSupplierName'),
            supplier_contact=request.POST.get('productSupplierContact'),
            supplier_code=request.POST.get('productSupplierCode'),
            lead_time=request.POST.get('productLeadTime')
        )
        product.save()
        print("Product registered successfully:", product.name)  # Added print statement
        message = "Product registered successfully!"
    return render(request, 'inventory.html', {'message': message})

