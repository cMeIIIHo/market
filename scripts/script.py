import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *