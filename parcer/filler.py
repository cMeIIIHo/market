import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
import django
django.setup()
from catalog.models import *
import json


def fill_product_in_db(product, category, mark):
    Product.objects.create(
        category=category,
        mark=mark,
        name=product['name'],
        description='\n'.join([line.replace('\xa0', ' ') for line in product['description'] if len(line) > 20])
    )


with open('vl_data.json', 'r') as f:
    data = json.load(f)
    for num, product in enumerate(data):
        print(num)
        for key in product:
            print(key, ' = ', product[key])
        product['Тип линз'] += " линзы"
        category = Category.objects.get_or_create(name=product['Тип линз'])
        if 'brand' in product:
            mark = Mark.objects.get_or_create(producer=product['producer'], brand=product['brand'])
        else:
            print(product['producer'])
            mark = Mark.objects.get_or_create(producer=product['producer'], brand='')
        fill_product_in_db(product, category, mark)

