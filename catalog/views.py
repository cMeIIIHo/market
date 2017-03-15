from django.shortcuts import get_object_or_404, render, render_to_response
from catalog.models import Sale_card
from catalog.models import *
import collections
from django.db.models import Max, Min
from django.template.context_processors import csrf

from django.db import connection
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template import RequestContext, loader
from django.views import generic
from django.utils import timezone

# Create your views here.


def index(request):
    context = {
        'sale_cards': Sale_card.objects.all(),
    }
    return render_to_response("catalog/index.html", context)


def product_filter(request, category_id=1):

    # get main category
    given_cat = get_object_or_404(Category, pk=category_id)

    # get children cats
    cat_list = list(given_cat.get_kids_generator())

    # get all the children's products
    products = Product.objects.filter(category__in=cat_list)

    # product's manufacturers
    manufacturers = Mark.objects.filter(product__in=products).distinct()

    # making filter-block. It uses a dict, filled with {Option names: [Option values]}
    filters = collections.OrderedDict()
    filter_names = Option_name.objects.filter(category__in=cat_list, usage_in_filters=True).distinct()
    for filter_name in filter_names:
        filters[filter_name] = filter_name.get_values().filter(spec_prod__product__in=products,
                                                               spec_prod__amount__gt=0).distinct()
        # if filter type =='interval', we need only 2 opt values - 'max' and 'min'
        if filter_name.appearance_in_filters == 'interval':
            min_and_max = filters[filter_name].aggregate(min=Min('value'), max=Max('value'))
            filters[filter_name] = filters[filter_name].filter(Q(value=min_and_max['min']) |
                                                               Q(value=min_and_max['max']))

    # apply activated filters to products
    for param_name, param_value in request.GET.items():
        param_name = param_name.split('-')
        if param_name[0] == 'cb' and param_name[2].isnumeric():
            if param_name[1] == 'category':
                products = products.filter(**{'category__id': int(param_name[2])}).distinct()
            elif param_name[1] == 'mark':
                products = products.filter(**{'mark__id': int(param_name[2])}).distinct()
            elif param_name[1] in ('float_opts', 'int_opts', 'text_opts'):
                products = products.filter(**{'spec_prod__%s__id' % param_name[1]: int(param_name[2])}).distinct()
        elif param_name[0] == 'interval' and param_value != '' and param_name[2].isnumeric() and param_name[3] in ('gte', 'lte'):
            if param_name[1] == 'float_opts':
                suitable_vals = Float_opt.objects.filter(**{'name__id': param_name[2],
                                                            'value__%s' % param_name[3]: float(param_value)}).distinct()
                products = products.filter(**{'spec_prod__%s__in' % param_name[1]: suitable_vals}).distinct()
            elif param_name[1] == 'int_opts':
                suitable_vals = Int_opt.objects.filter(**{'name__id': param_name[2],
                                                          'value__%s' % param_name[3]: int(param_value)}).distinct()
                products = products.filter(**{'spec_prod__%s__in' % param_name[1]: suitable_vals}).distinct()




            # try:
            #     param_value = int(param_value)
            # except ValueError:
            #     param_value = float(param_value)
            #     if param_name[1] in ('float_opt', 'int_opt', 'text_opt') and param_name[2].isnumeric() and param_name[3] in ('gt', 'lt'):
            #         suitable_value =


        # elif param_name[0] == 'interval' and param_value is not None:
        #     if param_name[1] in ('float_opt', 'int_opt', 'text_opt') and param_name[2].isnumeric() and param_name[3] in ('gt', 'lt'):
        #
        #         products = products.filter(**{'spec_prod__%s__name__id' % param_name[1]: int(param_name[2]),
        #                                       'spec_prod__%s__value__%s' % (param_name[1], param_name[3]): (param_value)})










    # for param_name, param_value in request.GET.items():
    #     param_name = param_name.split('-')
    #     if param_name[0] == 'cb':
    #         products = products.filter(**{'spec_prod__%s_opts__id' % param_name[1]: int(param_name[2])}).distinct()










    get_data = request.GET

    context = {
        'cat_list': cat_list,
        'filters': filters,
        'manufacturers': manufacturers,
        'products': products,
        'get_data': get_data,
    }
    return render_to_response('catalog/product_filter.html', context)



    # # received category
    # main_cat = Category.objects.get(name=category_name)
    #
    # # if it has children, list them
    # cats_to_filter = main_cat.category_set.all()
    #
    # # if it has not, just make it iterable
    # if not cats_to_filter:
    #     cats_to_filter = [main_cat]
    #
    # # make filters dictionary
    # filters = collections.OrderedDict()
    #
    # # fill dictionary with product_filter-block's names in correct order
    # filter_names = Option_name.objects.product_filter(category__in=cats_to_filter, usage_in_filters=True).distinct()
    # for filter_name in filter_names:
    #     filters[filter_name] = []
    #
    # # fill dictionary with filters values
    # for cat in cats_to_filter:
    #     for option in cat.int_opt_set.product_filter(name__in=filter_names):
    #         filters[option.name].append(option)
    #     for option in cat.text_opt_set.product_filter(name__in=filter_names):
    #         filters[option.name].append(option)
    #     for option in cat.float_opt_set.product_filter(name__in=filter_names):
    #         filters[option.name].append(option)
    #
    # context = {'filters': filters,}
    # return render_to_response('catalog/product_filter.html', context)

# def product_filter(request):
#     manufacturers = Mark.objects.product_filter(product__prod_type__name='Линзы').distinct()
#     lens_types = Sub_type.objects.product_filter(prod_type__name='Линзы')
#
#     #fina all option objects ( name+value) for lenses
#     int_opts = Int_opt.objects.product_filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()
#     text_opts = Text_opt.objects.product_filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()
#     float_opts = Float_opt.objects.product_filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()
#
#
#     # create a dict with remaiing filters (as color, size )
#     filters = collections.OrderedDict()
#
#     #firstly add product_filter names
#     filter_names = Option_name.objects.product_filter(sub_type__prod_type__name='Линзы', usage_in_filters=True).distinct()
#     for filter_name in filter_names:
#         filters[filter_name] = []
#
#     #secondly fill product_filter blocks with values
#     def fill_filter_block(opts):
#         for opt in opts:
#             filters[opt.name].append(opt)
#
#     fill_filter_block(int_opts)
#     fill_filter_block(text_opts)
#     fill_filter_block(float_opts)
#
#     context = {
#         'manufacturers': manufacturers,
#         'lens_types': lens_types,
#         'filters': filters,
#     }
#     return render_to_response('catalog/product_filter.html', context)