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
    products = Product.objects.filter(category__in=cat_list, spec_prod__amount__gt=0).distinct()

    # product's marks
    marks = Mark.objects.filter(product__in=products).distinct()

    # making filter-block. It uses a dict, filled with {Option names: [Option values]}
    filters = collections.OrderedDict()
    filter_names = Option_name.objects.filter(category__in=cat_list, usage_in_filters=True).distinct()
    for filter_name in filter_names:
        filters[filter_name] = filter_name.get_values().filter(spec_prod__product__in=products,
                                                               spec_prod__amount__gt=0).distinct()
        # if filter type =='interval', we need only 2 opt values - 'max' and 'min'
        if filter_name.appearance_in_filters == 'interval':
            filters[filter_name] = filters[filter_name].aggregate(gte=Min('value'), lte=Max('value'))

    for param, values in request.GET.lists():
        if param in ('mark', 'category'):
            suitable_opt_ids = [int(i) for i in values if i.isnumeric()]
            products = products.filter(**{'%s__id__in' % param: suitable_opt_ids}).distinct()
        else:
            try:
                border_type, opt_id, opt_type = param.split('-')
            except Exception:
                pass
            else:
                if border_type == 'equal' and opt_type in ('float', 'int', 'text'):
                    suitable_opt_ids = [int(i) for i in values if i.isnumeric()]
                    suitable_spec_prod_ids = Spec_prod.objects.filter(**{'%s_opts__id__in' % opt_type: suitable_opt_ids}).values_list('product').distinct()
                    products = products.filter(id__in=suitable_spec_prod_ids)
                elif border_type in ('lte', 'gte') and opt_id.isnumeric():
                    if opt_type == 'float':
                        try:
                            value = float(values[0])
                        except Exception:
                            pass
                        else:
                            suitable_opt_ids = Float_opt.objects.filter(**{'name__id': opt_id, 'value__%s' % border_type: value}).values_list('id').distinct()
                            suitable_spec_prod_ids = Spec_prod.objects.filter(**{'float_opts__id__in': suitable_opt_ids}).values_list('product').distinct()
                            products = products.filter(id__in=suitable_spec_prod_ids)
                    elif opt_type == 'int':
                        try:
                            value = int(values[0])
                        except Exception:
                            pass
                        else:
                            suitable_opt_ids = Int_opt.objects.filter(**{'name__id': opt_id, 'value__%s' % border_type: value}).values_list('id').distinct()
                            suitable_spec_prod_ids = Spec_prod.objects.filter(**{'int_opts__id__in': suitable_opt_ids}).values_list('product').distinct()
                            products = products.filter(id__in=suitable_spec_prod_ids)

    get_data = request.GET

    context = {
        'cat_list': cat_list,
        'filters': filters,
        'marks': marks,
        'products': products,
        'data': get_data,
    }
    return render_to_response('catalog/product_filter.html', context)



                # q_list = Q()
                # for value in values:
                #     q_list |= Q(**{'spec_prod__%s_opts__id' % opt_type: int(value)})
                # products = products.filter(q_list).distinct()

                # list_of_id = [int(i) for i in values]
                # products = products.filter(**{'spec_prod__%s_opts__id__in' % opt_type: list_of_id}).distinct()

            # elif border_type in ['more', 'less']:
            #     if opt_type == 'float':



    # for param, values in request.GET.lists():
    #     if param == 'mark' or param == 'category':
    #         q_list = Q()
    #         for value in values:
    #             q_list |= Q(**{'%s__id' % param: int(value)})
    #         products = products.filter(q_list).distinct()
    #
    #
    #         # list_of_id = [int(i) for i in values]
    #         # products = products.filter(**{'%s__id__in' % param: list_of_id}).distinct()
    #     else:
    #         border_type, opt_id, opt_type = param.split('-')
    #         if border_type == 'equal' and opt_type in ['float', 'int', 'text']:
    #             q_list = Q()
    #             for value in values:
    #                 q_list |= Q(**{'spec_prod__%s_opts__id' % opt_type: int(value)})
    #             products = products.filter(q_list).distinct()

                # list_of_id = [int(i) for i in values]
                # products = products.filter(**{'spec_prod__%s_opts__id__in' % opt_type: list_of_id}).distinct()

            # elif border_type in ['more', 'less']:
            #     if opt_type == 'float':
    # products = list(products)
    # products = [i for i in products]
    #










    # check = []
    # for param_key, param_value in request.GET.items():
    #     if param_key.startswith('cb-'):
    #         if param_key.count('-') == 2:
    #             elem_type, field_name, option_id = param_key.split('-')
    #             if option_id.isnumeric():
    #                 if field_name == 'category':
    #                     products = products.filter(**{'category__id': int(option_id)}).distinct()
    #                     check.append(1)
    #                 elif field_name == 'marks':
    #                     products = products.filter(**{'mark__id': int(option_id)}).distinct()
    #                     check.append(2)
    #                 elif field_name in ('float_opts', 'int_opts', 'text_opts'):
    #                     products = products.filter(**{'spec_prod__%s__id' % field_name: int(option_id)}).distinct()
    #                     check.append(3)
    #     elif param_key.startswith('interval-') and param_value != '':
    #         if param_key.count('-') == 3:
    #             elem_type, field_name, opt_name_id, gt_or_lt = param_key.split('-')
    #             if opt_name_id.isnumeric() and gt_or_lt in ('gte', 'lte') and field_name in ('float_opts', 'int_opts'):
    #                 if field_name == 'float_opts':
    #                     suitable_vals = Float_opt.objects.filter(**{'name__id': opt_name_id,
    #                                                                 'value__%s' % gt_or_lt: float(param_value)}).distinct()
    #                 else:
    #                     suitable_vals = Int_opt.objects.filter(**{'name__id': opt_name_id,
    #                                                               'value__%s' % gt_or_lt: int(param_value)}).distinct()
    #                 products = products.filter(**{'spec_prod__%s__in' % field_name: suitable_vals}).distinct()
    #                 check.append(4)




    # # apply activated filters to products
    # for param_name, param_value in request.GET.items():
    #
    #     # param name consists of some information, divided by '-'
    #     param_name = param_name.split('-')
    #
    #     # if html element was a checkbox
    #     if param_name[0] == 'cb' and param_name[2].isnumeric():
    #         if param_name[1] == 'category':
    #             products = products.filter(**{'category__id': int(param_name[2])}).distinct()
    #         elif param_name[1] == 'marks':
    #             products = products.filter(**{'mark__id': int(param_name[2])}).distinct()
    #         elif param_name[1] in ('float_opts', 'int_opts', 'text_opts'):
    #             products = products.filter(**{'spec_prod__%s__id' % param_name[1]: int(param_name[2])}).distinct()
    #
    #     # if html element was an interval and was filled with value
    #     elif param_name[0] == 'interval' and param_value != '' and param_name[2].isnumeric() and param_name[3] in ('gte', 'lte'):
    #         if param_name[1] == 'float_opts':
    #             suitable_vals = Float_opt.objects.filter(**{'name__id': param_name[2],
    #                                                         'value__%s' % param_name[3]: float(param_value)}).distinct()
    #             products = products.filter(**{'spec_prod__%s__in' % param_name[1]: suitable_vals}).distinct()
    #         elif param_name[1] == 'int_opts':
    #             suitable_vals = Int_opt.objects.filter(**{'name__id': param_name[2],
    #                                                       'value__%s' % param_name[3]: int(param_value)}).distinct()
    #             products = products.filter(**{'spec_prod__%s__in' % param_name[1]: suitable_vals}).distinct()

    get_data = request.GET

    context = {
        'cat_list': cat_list,
        'filters': filters,
        'marks': marks,
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
#     marks = Mark.objects.product_filter(product__prod_type__name='Линзы').distinct()
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
#         'marks': marks,
#         'lens_types': lens_types,
#         'filters': filters,
#     }
#     return render_to_response('catalog/product_filter.html', context)