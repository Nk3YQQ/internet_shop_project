import json

from django.core.management import BaseCommand

from catalog.models import Category, Product
from catalog.path import CATEGORIES_DATA_PATH, PRODUCTS_DATA_PATH


class Command(BaseCommand):
    @staticmethod
    def json_read_categories():
        with open(CATEGORIES_DATA_PATH, 'r', encoding='utf-8') as data:
            return list({'id': item['pk'], **item['fields']} for item in json.load(data))

    @staticmethod
    def json_read_products():
        with open(PRODUCTS_DATA_PATH, 'r', encoding='utf-8') as data:
            return list({'id': item['pk'], **item['fields']} for item in json.load(data))

    def handle(self, *args, **options):
        categories_data = self.json_read_categories()
        products_data = self.json_read_products()

        categories_dict = {}
        for category_data in categories_data:
            category_id = category_data.pop('id')
            category, created = Category.objects.get_or_create(id=category_id, defaults=category_data)
            categories_dict[category_id] = category

        products_to_create = []
        for product_data in products_data:
            category_id = product_data.pop('category')
            if category_id is not None:
                category = categories_dict.get(category_id)
                if category:
                    product = Product(category=category, **product_data)
                    products_to_create.append(product)

        Product.objects.bulk_create(products_to_create)
