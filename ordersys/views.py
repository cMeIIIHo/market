from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ordersys.models import ProxyUser, ProxyAnonymousUser
from django.http import Http404
from catalog.models import Spec_prod


def clear(data, data_type):
    """
    making sure that data has specified format or can be converted to it
    """
    if isinstance(data, data_type):
        return data
    else:
        try:
            data = data_type(data)
        except ValueError:
            raise Http404('unexpected data %s passed, could not convert to a suitable format %s' % (data, data_type))
        else:
            return data


def add_sp_to_cart(request):
    """
    product_page ajax function
    """
    sp_id = clear(request.POST.get('sp_id'), int)
    sp = get_object_or_404(Spec_prod, pk=sp_id)
    quantity = clear(request.POST.get('sp_quantity'), int)
    user = request.user
    if user.is_authenticated():
        user = ProxyUser.objects.get(pk=user.pk)               # ProxyUser is made to add some methods (below)
    else:
        user = ProxyAnonymousUser()
    if user.has_cart(request):                                 # this method,
        user.add_sp_to_cart(request, sp, quantity)             # this
    else:
        user.create_cart(request, sp, quantity)                # and this
    return HttpResponse()
