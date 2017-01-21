from django.shortcuts import get_object_or_404, render, render_to_response
from catalog.models import Sale_card
from catalog.models import *
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

    filters = Option_name.objects.filter(Q(int_opt__spec_prod__product__prod_type__name='Линзы') \
                                             | Q(text_opt__spec_prod__product__prod_type__name='Линзы') \
                                             | Q(float_opt__spec_prod__product__prod_type__name='Линзы')).distinct()

    context = {
        'filters': filters,
        'manufacturers': set(Mark.objects.filter(product__prod_type__name='Линзы')),
    }
    return render_to_response('catalog/filter.html', context)