import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *
import json
import requests
from django.core.files import File

opts = {
    'krivizna_options': 'Радиус кривизны',
    'Диаметр': 'Диаметр',
    'Влагосодержание': 'Влагосодержание',
    'DK/T': 'DK/T',
    'Упаковка': 'Упаковка',
    'Срок замены': 'Срок замены',
    'opt_force_options': 'Оптическая сила',
    'colors': 'Цвет',
    'axis': 'Ось',
    'cilinder': 'Цилиндр',
    'sphere': 'Сфера',
    'addidation': 'Аддидация',
    'name': 'name',
    'price': 'price',

}

#create new_data

with open('vl_data_2.json', 'r') as f:
    data = json.load(f)
    new_data = []
    count = 0
    for num, product in enumerate(data):
        new_product = {}
        for key, value in product.items():
            if key in opts:
                if key == 'price':
                    new_product[opts[key]] = int(''.join([i for i in product[key].split()]))
                else:
                    new_product[opts[key]] = product[key]
                count += 1
        if not new_product:
            print("DFSDFSDFSDF")
            break
        else:
            new_data.append(new_product)
    print('END____________END_______________END')

        # look at new_data

    # for num, new_product in enumerate(new_data):
    #     for key, value in new_product.items():
    #         print(key, value)
    #     print(num, '____________________________________________________')

# check features

    new_data[15]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[29]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[45]['Оптическая сила'] = [-float(i)/2 for i in range(1, 6)]
    new_data[45]['Цвет'] = ['Кошачий глаз красный', 'Пламя красно-желтое', 'Пламя черно-желтое']
    new_data[56]['Радиус кривизны'] = [8.6]
    new_data[58]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[65]['Радиус кривизны'] = [8.6]
    new_data[67]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[76]['Цвет'] = ['Черный ободок']
    new_data[80]['Оптическая сила'] = [0.0]
    new_data[81]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[83]['Радиус кривизны'] = [8.6]
    new_data[86]['Цвет'] = [
        'Aqua',
        'Green',
        'Blue',
        'Grey',
        'Chocolate',
        'Dark-Blue',
    ]
    new_data[89]['Цвет'] = [
        'Aqua',
        'Green',
        'Blue',
        'Grey',
        'Chocolate',
        'Dark-Blue',
    ]
    new_data[91]['Оптическая сила'] = [-float(i)/4 for i in range(1, 17)] + \
                                      [-float(i) / 2 for i in range(17, 50)] + \
                                      [float(i) / 4 for i in range(1, 17)] + \
                                      [float(i) / 2 for i in range(17, 50)]
    new_data[101]['Оптическая сила'] = [-float(i) / 4 for i in range(1, 17)] + \
                                      [-float(i) / 2 for i in range(17, 50)] + \
                                      [float(i) / 4 for i in range(1, 17)] + \
                                      [float(i) / 2 for i in range(17, 50)]
    new_data[104]['Радиус кривизны'] = [8.6]
    new_data[104]['Оптическая сила'] = [-float(i)/2 for i in range(21)]
    new_data[109]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[114]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[115]['Оптическая сила'] = [-float(i) / 4 for i in range(1, 17)] + \
                                      [-float(i) / 2 for i in range(17, 50)] + \
                                      [float(i) / 4 for i in range(1, 17)] + \
                                      [float(i) / 2 for i in range(17, 50)]
    new_data[122]['Оптическая сила'] = [0.0]
    new_data[123]['Цилиндр'] = [-0.75, -1.25, -1.75, -2.25]
    new_data[124]['Оптическая сила'] = [0.0]

    for num, p in enumerate(new_data):
        product = Product.objects.get(name=p['name'])
        opt_list = [opt.name for opt in product.category.opt_list.all()]
        for key, value in p.items():
            if key == 'price':
                print(key, type(value), value)
    #         if key not in opt_list and key != 'name':
    #             print(num, key)
    #             print(p['name'])
    #             print(data[num]['link'])
    #             print(data[num]['Тип линз'])
    #             print('____________________________________________________')
    # with open('vl_data_3.json', 'w') as f2:
    #     json.dump(new_data, f2)











