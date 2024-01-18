from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    sku = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    current_stock = models.IntegerField(validators=[MinValueValidator(0)])
    minimum_stock = models.IntegerField(validators=[MinValueValidator(0)])
    maximum_stock = models.IntegerField(validators=[MinValueValidator(0)])
    reorder_quantity = models.IntegerField(validators=[MinValueValidator(0)])
    stock_status = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    selling_price = models.FloatField(validators=[MinValueValidator(0.0)])
    cost_price = models.FloatField(validators=[MinValueValidator(0.0)])
    profit_margin = models.FloatField(validators=[MinValueValidator(0.0)])
    special_discounts = models.FloatField(validators=[MinValueValidator(0.0)])
    supplier_name = models.CharField(max_length=100)
    supplier_contact = models.CharField(max_length=100)
    supplier_code = models.CharField(max_length=50)
    lead_time = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        app_label = 'CashlessSoftwareDja1'
        db_table = 'Products'  # Specify the actual table name here