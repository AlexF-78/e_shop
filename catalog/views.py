from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
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
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно создан!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование товара"""
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    login_url = '/users/login/'

    def test_func(self):
        """Проверяет, что пользователь - владелец продукта"""
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        messages.error(self.request, 'Вы можете редактировать только свои товары!')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактировать товар: {self.object.name}'
        context['can_unpublish'] = self.request.user.has_perm('catalog.can_unpublish_product')
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.has_perm('catalog.can_unpublish_product'):
            form.fields['is_published'].disabled = True
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{self.object.name}" успешно обновлен!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление товара только для авторизованных пользователей"""
    model = Product
    template_name = 'product_confirm_delete.html'
    context_object_name = 'product'
    success_url = reverse_lazy('catalog:home')
    login_url = '/users/login/'

    def test_func(self):
        """Проверяет, может ли пользователь удалить продукт"""
        product = self.get_object()
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_delete_any_product'))

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого товара!')
        return redirect('catalog:product_detail', pk=self.get_object().pk)

    def form_valid(self, form):
        product_name = self.object.name
        response = super().form_valid(form)
        messages.success(self.request, f'Товар "{product_name}" успешно удален!')
        return response


class ProductUnpublishView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Отмена публикации продукта"""
    permission_required = 'catalog.can_unpublish_product'
    login_url = '/users/login/'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        if product.publish_status == 'published':
            product.publish_status = 'archived'
            product.save()
            messages.success(request, f'Товар "{product.name}" снят с публикации!')
        else:
            messages.info(request, f'Товар "{product.name}" уже не опубликован!')
        return redirect('catalog:product_detail', pk=product.pk)
