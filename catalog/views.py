
# from django.shortcuts import get_object_or_404,render
# from django.views import View
from django.views.generic import ListView, TemplateView, DetailView

from .models import Product, Category

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'


# def home(request):
#     # Получаем все товары для отображения на Главной
#     products = Product.objects.all()
#     return render(request, 'home.html', {'products': products})

class ContactView(TemplateView):
    template_name = 'contacts.html'

# def contact(request):
#     return render(request, 'contacts.html')


class ProductView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'

# def product_detail(request, pk):
#     product = get_object_or_404(Product,pk=pk)
#     return render(request, 'product_detail.html', {'product': product})
