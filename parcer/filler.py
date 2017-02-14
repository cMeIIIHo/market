import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
import django
django.setup()

from catalog.models import *
import json

with open('vl_data.json', 'r') as f:
    data = json.load(f)
    for product in data:
        product['Тип линз'] = product['Тип линз'] + " линзы"
        category = Category.objects.get_or_create(name=product['Тип линз'])


        for key in product:
            print(product[key])
