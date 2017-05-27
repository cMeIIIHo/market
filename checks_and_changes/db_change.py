import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django

django.setup()

from catalog.models import *
import random

product = Product.objects.get(name='Acuvue Oasys 6')
sps = product.spec_prod_set.all()
for sp in sps:
    # sp.price = random.randint(900, 1200)
    # sp.save()
    print(sp.price)
