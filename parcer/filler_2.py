import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *
import json
import requests
from django.core.files import File

from itertools import product
import random


# Opts = {
#     'krivizna_options': {'Радиус кривизны': 'float'},
#     'Диаметр': {'Диаметр': 'float'},
#     'Влагосодержание': {'Влагосодержание': 'int'},
#     'DK/T': {'DK/T': 'int'},
#     'Упаковка': {'Упаковка': 'int'},
#     'Срок замены': {'Срок замены': 'text'},
#     'opt_force_options': {'Оптическая сила': 'float'},
#     'colors': {'Цвет': 'text'},
#     'axis': {'Ось': 'int'},
#     'cilinder': {'Цилиндр': 'float'},
#     'sphere': {'Сфера': 'float'},
#     'addidation': {'Аддидация': 'text'},
# }

# Opts = {
#     'krivizna_options': 'Радиус кривизны',
#     'Диаметр': 'Диаметр',
#     'Влагосодержание': 'Влагосодержание',
#     'DK/T': 'DK/T',
#     'Упаковка': 'Упаковка',
#     'Срок замены': 'Срок замены',
#     'opt_force_options': 'Оптическая сила',
#     'colors': 'Цвет',
#     'axis': 'Ось',
#     'cilinder': 'Цилиндр',
#     'sphere': 'Сфера',
#     'addidation': 'Аддидация',
# }


def create_object(params):
    if 'name' in params:
        p = Product.objects.get(name=params.pop('name'))
        opt_list = [opt.name for opt in p.category.opt_list.all()]
        spec_prod = Spec_prod(
            product=p,
            price=params['price'],
            amount=random.randint(0, 15)
        )
        spec_prod.save()
        for opt, value in params.items():
            if opt in opt_list:
                if type(value) == str:
                    opt, created = Text_opt.objects.get_or_create(name=Option_name.objects.get(name=opt), value=value)
                    spec_prod.text_opts.add(opt)
                if type(value) == int:
                    opt, created = Int_opt.objects.get_or_create(name=Option_name.objects.get(name=opt), value=value)
                    spec_prod.int_opts.add(opt)
                if type(value) == float:
                    opt, created = Float_opt.objects.get_or_create(name=Option_name.objects.get(name=opt), value=value)
                    spec_prod.float_opts.add(opt)






with open('vl_data_3.json', 'r') as f:
    data = json.load(f)
    print(len(data))
    data = data[80:120]
    for num, aq in enumerate(data):
        params = list(aq.keys())
        values = [(v if isinstance(v, list) else [v]) for v in aq.values()]
        count = 0

        vars = list(product(*values))
        if len(vars) >= 100:
            vars = random.sample(vars, 99)
        for set_values in vars:
            create_object(dict(zip(params, set_values)))
        print(num, 'product created_____________________')










            # count += 1
            # for p, s in zip(params, set_values):
            #
            #     Spec_prod.objects.create
            #     print(p, s)
            # print('_________________________________', count)








    #     iterable_params = [key for key in product if type(product[key]) == list]
    #     non_iterable_params = [key for key in product if type(product[key]) is not list]
    #     it_set = it_set.union(set(iterable_params))
    #     non_it_set = non_it_set.union(set(non_iterable_params))
    #     print(product['link'])
    #     print(iterable_params)
    #     print(non_iterable_params)
    # print(it_set)
    # print(non_it_set)





