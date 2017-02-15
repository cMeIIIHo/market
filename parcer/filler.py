import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django
django.setup()

from catalog.models import *
import json
import requests

''' getting info from json file. Still in incorrect form,
so have to do some magic. After manipulations with data form,
i save it as Product object. Each Product got some features, so
after being created, i loop its features and create some Spec_prod
objects - look models. '''


def get_pict(prod, pic_type):
    name = '{}_for_{}'.format(pic_type, prod['name'])
    with open(name, 'wb') as f:
        pic = requests.get(prod[pic_type]).content
        f.write(pic)
    return name

with open('vl_data.json', 'r') as f:
    data = json.load(f)
    for num, product in enumerate(data):
        print(num)
        for key in product:
            print(key, ' = ', product[key])

        # get prod.type in a correct form
        product['Тип линз'] += " линзы"
        category = Category.objects.get_or_create(name=product['Тип линз'])[0]

        # get prod's brand
        if 'brand' in product:
            mark = Mark.objects.get_or_create(producer=product['producer'], brand=product['brand'])[0]
        else:
            print(product['producer'])
            mark = Mark.objects.get_or_create(producer=product['producer'], brand='')[0]

        # get picts
        picture = get_pict(product, 'picture')
        banner = get_pict(product, 'banner')

        # create Product object
        Product.objects.get_or_create(
            category=category,
            mark=mark,
            name=product['name'],
            description='\n'.join([line.replace('\xa0', ' ') for line in product['description'] if len(line) > 20]),
            # TODO are u sure its gonna be in defaults? mby try DB delete
            defaults={
                'picture': picture,
                'banner': banner,
            },

        )

