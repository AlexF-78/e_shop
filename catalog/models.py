from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    """Модель категории товаров"""

    name = models.CharField(
        max_length=100,
        verbose_name='наименование'
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""

    PUBLISH_STATUS = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('archived', 'В архиве'),
    ]

    publish_status = models.CharField(
        max_length=20,
        choices=PUBLISH_STATUS,
        default='draft',  # по умолчанию черновик
        verbose_name='Статус публикации'
    )

    name = models.CharField(
        max_length=100,
        verbose_name='наименование'
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='изображение',
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        verbose_name='категория',
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена за покупку'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='дата последнего изменения'
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активный'
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        verbose_name='Владелец',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']
        permissions = [
            ("can_unpublish_product", "Может отменять публикацию продукта"),
            ("can_delete_any_product", "Может удалять любой продукт"),
        ]

    def __str__(self):
        return self.name
