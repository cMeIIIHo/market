import json

with open('vl_data.json', 'r') as f:
    data = json.load(f)
    new_data = []
    for num, product in enumerate(data):
        for key in product:
            #print(key, ' = ', product[key])
            if key == 'Влагосодержание':
                string = ''
                for liter in product[key]:
                    if liter.isnumeric():
                            string += liter
                product[key] = int(string[0:2])
                # print(key, ' = ', product[key], type(product[key]))
            if key == 'opt_force_options':
                list = []
                for val in product[key]:
                    val = val.split()[0]
                    val = float(val)
                    list.append(val)
                product[key] = list
                # print(key, ' = ', product[key])
            if key == 'DK/T':
                product[key] = int(''.join([i for i in product[key].split('.')[0] if i.isnumeric()]))
                # print(key, ' = ', product[key])
            if key == 'Диаметр':
                product[key] = float(product[key].split(';')[0])
                # print(key, ' = ', product[key], type(product[key]))
            if key == 'krivizna_options':
                product[key] = [float(i.split()[0]) for i in product[key]]
                #print(key, ' = ', product[key], type(product[key]))
            if key == 'Срок замены':
                #print(key, ' = ', product[key], type(product[key]))
                pass
            if key == 'sphere':
                product[key] = [float(i) for i in product[key]]
                #print(key, ' = ', product[key], type(product[key]))
            if key == 'Упаковка':
                product[key] = int(product[key].split()[0])
                #print(key, ' = ', product[key], type(product[key]))
            if key == 'axis':
                product[key] = [int(i) for i in product[key]]
                #print(key, ' = ', product[key], type(product[key]))
            if key == 'cilinder':
                product[key] = [float(i) for i in product[key]]
                #print(key, ' = ', product[key], type(product[key]))
            if key == 'opt_force_options':
                product[key] = [float(i) for i in product[key]]
                # print(key, ' = ', product[key], type(product[key]))
        new_data.append(product)
    for product in new_data:
        for key in product:
            print(key, ' = ', product[key])


    with open('vl_data_2.json', 'w') as f:
        json.dump(new_data, f, indent=4, sort_keys=True)








