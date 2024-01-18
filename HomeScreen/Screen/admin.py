# myapp/admin.py
from django.contrib import admin
from .models import Product, Transaction, Category

admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(Category)
