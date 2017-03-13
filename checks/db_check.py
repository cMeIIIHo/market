import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *

# sps = Spec_prod.objects.filter(float_opts__value=8.0).distinct()
# ps = Product.objects.filter(spec_prod__in=sps).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# ps = Product.objects.filter(spec_prod__float_opts__value=8.0).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# ps = Product.objects.filter(spec_prod__float_opts__id=188).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# fo = Float_opt.objects.filter(name__name='Радиус кривизны').filter(value=8.0)
# ps = Product.objects.filter(spec_prod__float_opts=fo).distinct()
# print(len(ps))
# for p in ps:
#     print(p)