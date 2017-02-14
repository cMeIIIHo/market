import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')
import django
django.setup()

from catalog.models import *
import json

with open('vl_data.json', 'r') as f:
    data = json.load(f)
    for product in data:
        category = Category.objects.get_or_create(name=product['Тип линз'])
