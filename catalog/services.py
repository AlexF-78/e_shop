from django.core.cache import cache

from catalog.models import Product


class ProductService:

    @staticmethod
    def get_products_by_category(category_id):
        """Возвращает список продуктов по категории"""
        cache_key = f'products_category_{category_id}'
        products = cache.get(cache_key)

        if not products:
            products = Product.objects.filter(
                category_id=category_id,
                is_published=True,
            )
            cache.set(cache_key, products, 60 * 15)
        return products


