from django.shortcuts import render
from .models import Product, Transaction


# screen/views.py

def home(request):
    # Your view logic here
    return render(request, 'home.html')



def home(request):
    products = Product.objects.all()
    transactions = Transaction.objects.all()
    context = {
        'products': products,
        'transactions': transactions,
    }
    return render(request, 'home.html', context)
