from django.shortcuts import get_object_or_404,render
from .models import Product, Category


def home(request):
    # Получаем все товары для отображения на Главной
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def contact(request):
    return render(request, 'contacts.html')

def product_detail(request, pk):
    product = get_object_or_404(Product,pk=pk)
    return render(request, 'product_detail.html', {'product': product})


