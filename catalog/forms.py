from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):
    # Список запрещённых слов
    FORBIDDEN_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price', 'is_published', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите наименование товара'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите описание товара'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену'
            }),
        }
        labels = {
            'name': 'Наименование товара',
            'description': 'Описание товара',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена',
            'is_published': 'Опубликовано',
            'is_active': 'Активный'
        }

    def __init__(self, *args, **kwargs):
        """Стилизация всех полей формы"""
        super().__init__(*args, **kwargs)

        # Базовые классы для всех полей
        base_input_class = 'form-control form-control-lg'
        base_select_class = 'form-select form-select-lg'
        base_textarea_class = 'form-control form-control-lg'
        base_file_class = 'form-control form-control-lg'
        base_checkbox_class = 'form-check-input'

        # Стилизация каждого поля
        self.fields['name'].widget.attrs.update({
            'class': base_input_class,
            'placeholder': 'Введите название товара...',
            'autofocus': True
        })

        self.fields['description'].widget.attrs.update({
            'class': base_textarea_class,
            'placeholder': 'Опишите товар подробно...',
            'rows': 4,
            'style': 'resize: vertical; min-height: 120px;'
        })

        self.fields['image'].widget.attrs.update({
            'class': base_file_class,
            'accept': 'image/*'
        })

        self.fields['category'].widget.attrs.update({
            'class': base_select_class,
        })

        self.fields['price'].widget.attrs.update({
            'class': base_input_class,
            'placeholder': '0.00'
        })

        # Стилизация булевых полей (чекбоксов)
        self.fields['is_published'].widget.attrs.update({
            'class': base_checkbox_class,
        })

        self.fields['is_active'].widget.attrs.update({
            'class': base_checkbox_class,
        })

        # Подсказки для полей
        self.fields['name'].help_text = 'Укажите краткое и понятное название товара'
        self.fields['description'].help_text = 'Максимально подробно опишите характеристики товара'
        self.fields['image'].help_text = 'Загрузите качественное изображение товара'
        self.fields['category'].help_text = 'Выберите подходящую категорию'
        self.fields['price'].help_text = 'Укажите цену в рублях'
        self.fields['is_published'].help_text = 'Сделать товар видимым для покупателей'
        self.fields['is_active'].help_text = 'Разрешить покупку этого товара'

    def clean_name(self):
        """Валидация названия товара"""
        name = self.cleaned_data.get('name', '')
        self.check_forbidden_words(name, 'наименовании')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description', '')
        self.check_forbidden_words(description, 'описании')
        return description

    def clean_price(self):
        """Кастомная валидация цены - проверка на отрицательные значения"""
        price = self.cleaned_data.get('price')

        # Проверка, что цена не отрицательная
        if price is not None and price < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной. Пожалуйста, введите положительное значение.'
            )

        return price

    def check_forbidden_words(self, text, field_name):
        """Проверка на наличие запрещённых слов"""
        if not text:
            return
        text_lower = text.lower()

        for forbidden_word in self.FORBIDDEN_WORDS:
            if forbidden_word in text_lower:
                raise forms.ValidationError(
                    f'Обнаружено запрещённое слово "{forbidden_word}" в "{field_name}" товара.'
                    f'Пожалуйста, удалите его и попробуйте снова.'
                )
