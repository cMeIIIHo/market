import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
import django
django.setup()
from catalog.models import *
import json


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



        for key in product:
            print(key, ' = ', product[key])
