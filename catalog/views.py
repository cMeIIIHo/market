from django.shortcuts import get_object_or_404, render, render_to_response
from catalog.models import Sale_card
from catalog.models import *
import collections
from django.db.models import Max, Min
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
        'lens_id': Category.objects.get(name='Линзы').id,
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

    # making filter-block. It use a dict, filled with {Option names: [Option values]}
    filters = collections.OrderedDict()
    filter_names = Option_name.objects.filter(category__in=cat_list, usage_in_filters=True).distinct()
    for filter_name in filter_names:
        if filter_name.appearance_in_filters == 'interval':
            min_and_max = filter_name.get_values().aggregate(min_value=Min('value'),
                                                             max_value=Max('value'))
            filters[filter_name] = [min_and_max['min_value'], min_and_max['max_value']]
        else:
            filters[filter_name] = filter_name.get_values().filter(spec_prod__product__in=products,
                                                                   spec_prod__amount__gt=0).distinct()
    context = {
        'cat_list': cat_list,
        'filters': filters,
        'manufacturers': manufacturers,
        'products': products,
        'lens_id': Category.objects.get(name='Линзы').id,
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