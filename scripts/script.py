import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *
from ordersys.models import *

model = OrderItem
obj = model.objects.get()
print(obj.order)