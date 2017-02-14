import json


with open('vl_data.json', 'r') as f:
    data = json.load(f)
    for product in data:
        for key in product:
            print(key + ' = ', product[key])
