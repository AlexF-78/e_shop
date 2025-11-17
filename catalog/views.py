from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# from django.shortcuts import get_object_or_404,render
# from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from .models import Product, Category

class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        """Оптимизируем запрос, загружая связанные категории"""
        return Product.objects.all()


class ContactView(TemplateView):
    template_name = 'contacts.html'


class ProductView(LoginRequiredMixin, DetailView):
    """ Просмотр деталей товара только для авторизованных пользователей"""
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    login_url = '/users/login/'

    def get_queryset(self):
        """Оптимизируем запрос, загружая связанные категории"""
        return Product.objects.all()


class ProductListView(ListView):
    """Список всех товаров"""
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.all().order_by('name')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового товара только для авторизованных пользователей"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    login_url = '/users/login/'


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Устанавливаем queryset для категорий
        form.fields['category'].queryset = Category.objects.all()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создать новый товар'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно создан!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    login_url = '/users/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать товар: {self.object.name}'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление товара только для авторизованных пользователей"""
    model = Product
    template_name = 'product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def form_valid(self, form):
        product_name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{product_name}" успешно удален!')
        return response

# def product_detail(request, pk):
#     product = get_object_or_404(Product,pk=pk)
#     return render(request, 'product_detail.html', {'product': product})
