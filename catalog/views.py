from django.shortcuts import get_object_or_404, render, render_to_response
from catalog.models import Sale_card
from catalog.models import *
import collections
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
    manufacturers = Mark.objects.filter(product__prod_type__name='Линзы').distinct()
    lens_types = Sub_type.objects.filter(prod_type__name='Линзы')

    #fina all option objects ( name+value) for lenses
    int_opts = Int_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()
    text_opts = Text_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()
    float_opts = Float_opt.objects.filter(spec_prod__product__prod_type__name='Линзы', name__usage_in_filters=True).distinct()


    # create a dict with remaiing filters (as color, size )
    filters = collections.OrderedDict()

    #firstly add filter names
    filter_names = Option_name.objects.filter(sub_type__prod_type__name='Линзы', usage_in_filters=True).distinct()
    for filter_name in filter_names:
        filters[filter_name] = []

    #secondly fill filter blocks with values
    def fill_filter_block(opts):
        for opt in opts:
            filters[opt.name].append(opt)

    fill_filter_block(int_opts)
    fill_filter_block(text_opts)
    fill_filter_block(float_opts)

    context = {
        'manufacturers': manufacturers,
        'lens_types': lens_types,
        'filters': filters,
    }
    return render_to_response('catalog/filter.html', context)