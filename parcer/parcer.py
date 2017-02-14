from bs4 import BeautifulSoup
import requests
import json

BASE_URL = 'https://viplinza.ru'


def get_main_html():
    # r = requests.get(url)
    # return r.text
    with open('html.txt', 'r') as f:
        return f.read()


def get_html(url):
    r = requests.get(url)
    return r.text


def parse(html):
    prod_list = []
    soup = BeautifulSoup(html)
    table = soup.find('div', class_='component centerblock')

    # get all product's HTML parts
    products = table.find_all('td', class_='producttd valign-top')
    counter = 0
    for num, product in enumerate(products):
        product_dict = {}
        title = product.find('h3', class_='producttitle')
        if title is not None:
            counter += 1

            # get product's link
            link = title.find('a')
            sub_href = link.get('href')
            full_link = BASE_URL + sub_href
            print(counter, full_link)
            product_dict['link']=full_link

            # get product's page
            product_soup = BeautifulSoup(get_html(full_link))
            prod_info = product_soup.find('div', class_="product-page")
            prod_left_block = prod_info.find('div', class_='product-left-block')

            # get prod IMG-link
            img = prod_left_block.find('img')
            img_link = img.get('src')
            print(img_link)
            product_dict['picture'] = img_link

            # get prod's producer and brand
            prod_and_brand = prod_left_block.find_all('a', class_='product-manufacturer')
            producer = prod_and_brand[0].text
            print(producer)
            product_dict['producer'] = producer
            try:
                brand = prod_and_brand[1].text
                print(brand)
                product_dict['brand'] = brand
            except IndexError:
                pass
            prod_right_block = prod_info.find('div', class_='product-right-block')

            # get prod's name
            name = prod_right_block.find('h1').text
            print(name)
            product_dict['name'] = name

            # get prod's price
            price = prod_right_block.find('span', class_='productPrice').text
            print(price)
            product_dict['price'] = price

            # get prod's "радиус кривизны" if it exists
            radius_krivizni_field = prod_right_block.find('select', id='Радиус_кривизны_field')
            if radius_krivizni_field is not None:
                krivizna_options = radius_krivizni_field.find_all('option')
                product_dict['krivizna_options'] = [k_opt.text for k_opt in krivizna_options]
                print(product_dict['krivizna_options'])

            # get color if it exists
            color_field = prod_right_block.find(id="Цвет_field")
            if color_field is not None:
                colors = [color.text for color in color_field.find_all('option')]
                product_dict['colors'] = colors
                print(product_dict['colors'])

            # get prod's optical force, if it exists
            opt_force_filed = prod_right_block.find('select', id='Оптическая_сила_field')
            if opt_force_filed is not None:
                opt_force_options = opt_force_filed.find_all('option')
                product_dict['opt_force_options'] = [opt_f_opt.text for opt_f_opt in opt_force_options]
                print(product_dict['opt_force_options'])

            # get prod's axis, if it exists
            axis_field = prod_right_block.find('select', id='Ось_field')
            if axis_field is not None:
                axis_options = axis_field.find_all('option')
                product_dict['axis'] = [axis.text for axis in axis_options]
                print(product_dict['axis'])

            # get prod's cylinder, if it exists
            cilinder_field = prod_right_block.find('select', id='Цилиндр_field')
            if cilinder_field is not None:
                cilinder_options = cilinder_field.find_all('option')
                product_dict['cilinder'] = [cilinder.text for cilinder in cilinder_options]
                print(product_dict['cilinder'])

            # get prod's sphere, if it exists
            sphere_field = prod_right_block.find('select', id='Сфера_field')
            if sphere_field is not None:
                sphere_options = sphere_field.find_all('option')
                product_dict['sphere'] = [sphere.text for sphere in sphere_options]
                print(product_dict['sphere'])

            # get prod's addidation, if it exists
            addidation_field = prod_right_block.find('select', id='Аддидация_field')
            if addidation_field is not None:
                addidation_options = addidation_field.find_all('option')
                product_dict['addidation'] = [addidation.text for addidation in addidation_options]
                print(product_dict['addidation'])

            # find pro's additional attributes
            attrs_table = prod_right_block.find('table', class_='table product-attr-table')
            attrs = attrs_table.find_all('tr')

            # parse em
            for attr in attrs:
                name, value = attr.find_all('td')
                product_dict[name.text] = value.text
                print(name.text, ' = ', product_dict[name.text])

            # find prod's extra additional attributes
            extra_attrs_table = prod_right_block.find('table', class_='product-attr-ext')
            extra_attrs = extra_attrs_table.find_all('tr')
            for attr in extra_attrs:
                name, value = attr.find_all('td')
                product_dict[name.text] = value.text
                print(name.text, ' = ', product_dict[name.text])

            # get banner link if it exists
            description_block = product_soup.find(id="product-additional-info-desc")
            banner = description_block.find('img')
            if banner is not None:
                banner = banner.get('src')
                if not banner.startswith('http'):
                    banner = BASE_URL + banner
                product_dict['banner'] = banner
                print(product_dict['banner'])

            # get description text
            texts = description_block.find_all('p')
            product_dict['description'] = [text.get_text() for text in texts if text.string is not None and not ""]
            print(product_dict['description'])



            prod_list.append(product_dict)

    with open('vl_data.json', 'w') as f:
        json.dump(prod_list, f, indent=4, sort_keys=True)


def main():
    parse(get_main_html())


if __name__ == '__main__':
    main()
