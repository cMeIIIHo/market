from django.shortcuts import get_object_or_404, render
from catalog.models import *
import collections
from utils import MyPaginator
from django.core.paginator import InvalidPage
from django.http import JsonResponse
from django.http import Http404
from funcs import turn_integer, check_positive


# Create your views here.


def index(request):
    context = {'sale_cards': Sale_card.objects.all(),
               'lens_category_id': Category.objects.get(name='Линзы').id}
    return render(request, "catalog/index.html", context)


def fill_filter_dict(filter_dict, option_names, products):
    for name in option_names:
        option_values = name.get_values().filter(spec_prod__product__in=products, spec_prod__amount__gt=0).distinct()
        if name.appearance_in_filters in ('1 col', '2 col'):
            filter_dict[name] = option_values
        elif name.appearance_in_filters == 'interval':
            last_index = option_values.count() - 1
            filter_dict[name] = [option_values[0], option_values[last_index]]
    return filter_dict


def validate_filter_request_data(data, option_names):
    valid_data = {}
    keys = data.keys()
    if 'category' in keys:
        valid_data['category'] = [int(i) for i in data.getlist('category') if i.isnumeric()]
    if 'mark' in keys:
        valid_data['mark'] = [int(i) for i in data.getlist('mark') if i.isnumeric()]
    for name in option_names:
        if str(name.id) in keys:
            if name.appearance_in_filters in ('1 col', '2 col'):
                valid_data[name.id] = [int(i) for i in data.getlist(str(name.id)) if i.isnumeric()]
            elif name.appearance_in_filters == 'interval' and data.getlist(str(name.id)) != ['', '']:
                type_func = {'float': float, 'int': int, 'text': str}[name.data_type]
                valid_data[name.id] = {}
                for i in range(2):
                    value = data.getlist(str(name.id))[i]
                    try:
                        value = type_func(value)
                    except ValueError:
                        pass
                    else:
                        valid_data[name.id][('gte', 'lte')[i]] = value
    return valid_data


def update_filter_dict_with_get_data(filter_dict, data):
    keys = data.keys()
    for name, values in filter_dict.items():
        if name.id in keys:
            if name.appearance_in_filters in ('1 col', '2 col'):
                for value in values:
                    if value.id in data[name.id]:
                        setattr(value, 'checked', 'checked')
                    else:
                        setattr(value, 'checked', '')
            elif name.appearance_in_filters == 'interval':
                setattr(values[0], 'checked', data[name.id].get('gte', ''))
                setattr(values[1], 'checked', data[name.id].get('lte', ''))
        else:
            for value in values:
                setattr(value, 'checked', '')


def update_marks_and_cat_list_with_get_data(cats, marks, data):
    keys = data.keys()
    c_and_m = {'category': cats, 'mark': marks}
    for key, values in c_and_m.items():
        if key in keys:
            for value in values:
                if value.id in data[key]:
                    setattr(value, 'checked', 'checked')
                else:
                    setattr(value, 'checked', '')
        else:
            for value in values:
                setattr(value, 'checked', '')


def filter_products_with_get_data(data, products, filter_names):
    keys = data.keys()
    if 'category' in keys:
        products = products.filter(**{'%s__id__in' % 'category': data['category']}).distinct()
    if 'mark' in keys:
        products = products.filter(**{'%s__id__in' % 'mark': data['mark']}).distinct()
    for name in filter_names:
        if name.id in keys:
            if name.appearance_in_filters in ('1 col', '2 col'):
                suitable_spec_prod_ids = Spec_prod.objects.filter(**{'%s_opts__id__in' % name.data_type: data[name.id]}).values_list('product').distinct()
                products = products.filter(id__in=suitable_spec_prod_ids)
            if name.appearance_in_filters == 'interval':
                if name.data_type == 'float':
                    for border, value in data[name.id].items():
                        suitable_opt_ids = Float_opt.objects.filter(**{'name__id': name.id, 'value__%s' % border: value}).values_list('id').distinct()
                        suitable_spec_prod_ids = Spec_prod.objects.filter(**{'float_opts__id__in': suitable_opt_ids}).values_list('product').distinct()
                        products = products.filter(id__in=suitable_spec_prod_ids)
                elif name.data_type == 'int':
                    for border, value in data[name.id].items():
                        suitable_opt_ids = Int_opt.objects.filter(**{'name__id': name.id, 'value__%s' % border: value}).values_list('id').distinct()
                        suitable_spec_prod_ids = Spec_prod.objects.filter(**{'int_opts__id__in': suitable_opt_ids}).values_list('product').distinct()
                        products = products.filter(id__in=suitable_spec_prod_ids)
    return products


def product_filter(request, category_id=1, page_number=1):
    # get main category
    given_cat = get_object_or_404(Category, pk=category_id)

    # get children cats
    cat_list = list(given_cat.get_kids_generator())

    # get all the children's products
    products = Product.objects.filter(category__in=cat_list, spec_prod__amount__gt=0).distinct()

    # product's marks
    marks = Mark.objects.filter(product__in=products).distinct()

    # making filter-block. It uses a dict, filled with {Option names: [Option values]}
    filters = collections.OrderedDict()
    filter_names = Option_name.objects.filter(category__in=cat_list, usage_in_filters=True).distinct()

    # fill a dict {Option_names: [Option_values]}
    filters = fill_filter_dict(filters, filter_names, products)

    # validate and change(easier to use in future) incoming filter(request=GET) data
    get_data = validate_filter_request_data(request.GET, filter_names)

    # use valid get_data to update filters(add attribute .checked to all filter_value objects)
    update_filter_dict_with_get_data(filters, get_data)

    # use valid get_data to update categories and marks(add attribute .checked to all objects)
    update_marks_and_cat_list_with_get_data(cat_list, marks, get_data)

    # apply filters from get_data to products
    products = filter_products_with_get_data(get_data, products, filter_names)

    # paginaition
    paginator = MyPaginator(products, 18)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)

    page.params = request.GET.urlencode()

    context = {
        'cat_list': cat_list,
        'filters': filters,
        'marks': marks,
        'page': page,
        'category_id': category_id,
        'lens_category_id': Category.objects.get(name='Линзы').id,
    }
    return render(request, 'catalog/product_filter.html', context)


def product_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'catalog/product_page.html', context)


# product_page, ajax function
def get_price(request):
    response_data = {}
    product_id = turn_integer(request.POST.get('product_id', 'empty'))
    product = get_object_or_404(Product, pk=product_id)
    spec_prods = product.spec_prod_set.filter(amount__gt=0)
    for option_name_id, type_opt_id in request.POST.items():
        if option_name_id.isdigit() and type_opt_id.isdigit():
            option_name = get_object_or_404(Option_name, pk=turn_integer(option_name_id))
            # type_func = {'float': float, 'int': int, 'text': str}[option_name.data_type]
            spec_prods = spec_prods.filter(**{'%s_opts__id' % option_name.data_type: turn_integer(type_opt_id)})
    if spec_prods.count() == 1:
        chosen_sp = spec_prods[0]
        amount = check_positive(turn_integer(request.POST.get('amount')))
        response_data['price'] = chosen_sp.price * amount
        response_data['spec_prod_id'] = chosen_sp.id
    elif spec_prods.count() == 0:
        response_data['error_message'] = 'SORRY... out of stock'
    elif spec_prods.count() > 1:
        raise Http404('too many spec_prods... there is a mistake in database ( same spec_prod in different lines - doubleing )')
    return JsonResponse(response_data)


