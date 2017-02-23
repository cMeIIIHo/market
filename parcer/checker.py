import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from itertools import product
import random

from catalog.models import *

# products = Product.objects.all()
# count = 0
# for product in products:
#     items = product.spec_prod_set.all()
#     if items.exists():
#         count += 1
#     print('%s ___has___ %s items' % (product.name, len(items)))
# print(count)

import json
#
# with open('vl_data_3.json', 'r') as f:
#     data = json.load(f)
#     print(len(data))
#     for p in data:
#         if p['name'] == 'Acuvue Oasys for astigmatism':
#             for opt, value in p.items():
#                 print(opt, ' = ', value)
#
# os = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180]
# cil = [-0.75, -1.25, -1.75, -2.25, -2.75]
# sphe = [0.0, -0.25, -0.5, -0.75, -1.0, -1.25, -1.5, -1.75, -2.0, -2.25, -2.5, -2.75, -3.0, -3.25, -3.5, -3.75, -4.0, -4.25, -4.5, -4.75, -5.0, -5.25, -5.5, -5.75, -6.0, -6.5, -7.0, -7.5, -8.0, -8.5, -9.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0, 4.25, 4.5, 4.75, 5.0, 5.25, 5.5, 5.75, 6.0]
# print(len(os), len(sphe), len(cil), len(os)*len(sphe)*len(cil))

# with open('vl_data_3.json', 'r') as f:
#     data = json.load(f)
#     print(len(data))
#     # data = data[80:120]
#     items = 0
#     for num, aq in enumerate(data):
#         params = list(aq.keys())
#         values = [(v if isinstance(v, list) else [v]) for v in aq.values()]
#         count = 0
#
#         vars = list(product(*values))
#         if len(vars) >= 100:
#             vars = random.sample(vars, 99)
#         items += len(vars)
#     print(items)

