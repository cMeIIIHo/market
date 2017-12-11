import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *
from ordersys.models import *
import random

# sps = Spec_prod.objects.all()
# for sp in sps:
#     sp.price = random.randint(100, 300)
#     sp.save()

sps = Spec_prod.objects.all()
for sp in sps:
    print(sp.price)


