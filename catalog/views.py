from django.shortcuts import get_object_or_404, render, render_to_response
from catalog.models import Sale_card
from catalog.models import *
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
        'sale_cards': Sale_card.objects.all()
    }
    return render_to_response("catalog/index.html", context)

def filter(request):
    # int_filters = Option_name.objects.filter(int_opt__spec_prod__product__prod_type__name='Линзы')
    # text_filters = Option_name.objects.filter(text_opt__spec_prod__product__prod_type__name='Линзы')
    # float_filters = Option_name.objects.filter(float_opt__spec_prod__product__prod_type__name='Линзы')
    # filters = set(list(int_filters) + list(text_filters) + list(float_filters))

    # filters = set(Option_name.objects.filter(Q(int_opt__spec_prod__product__prod_type__name='Линзы') \
    #                                          | Q(text_opt__spec_prod__product__prod_type__name='Линзы') \
    #                                          | Q(float_opt__spec_prod__product__prod_type__name='Линзы')))

    # i = Sub_type.objects.get(pk=1)
    # filters = i.opt_list.all()

    # i = Option_name.objects.get(pk=1)
    # filters = i.sub_type_set.all()



    # filter_names = Option_name.objects.filter(Q(int_opt__spec_prod__product__prod_type__name='Линзы') \
    #                                          | Q(text_opt__spec_prod__product__prod_type__name='Линзы') \
    #                                          | Q(float_opt__spec_prod__product__prod_type__name='Линзы')).distinct()\
    #                                         .filter(usage_in_filters=True).values('name')

    int_opts = Int_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).select_related('name')
    text_opts = Text_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).select_related('name')
    float_opts = Float_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).select_related('name')

    # for filter_name in filter_names:
    #     filters[filter_name] =

    filters = {}

    def add_filter_block(filter_opts):
        for filter_opt in filter_opts:
            if filter_opt.name.name in filters.keys():
                filters[filter_opt.name.name].append(filter_opt.value)
            else:
                filters[filter_opt.name.name] = [filter_opt.value]

    add_filter_block(int_opts)
    add_filter_block(text_opts)
    add_filter_block(float_opts)


    context = {
        'filters': filters,
        'manufacturers': set(Mark.objects.filter(product__prod_type__name='Линзы')),
    }
    return render_to_response('catalog/filter.html', context)