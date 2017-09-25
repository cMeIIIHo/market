from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ordersys.models import ProxyUser, ProxyAnonymousUser
from catalog.models import Spec_prod
from funcs import clean_data


def add_sp_to_cart(request):
    """
    product_page ajax function
    """
    sp_id = clean_data(request.POST.get('sp_id'), int)
    sp = get_object_or_404(Spec_prod, pk=sp_id)
    quantity = clean_data(request.POST.get('sp_quantity'), int)
    user = request.user
    if user.is_authenticated():
        user = ProxyUser.objects.get(pk=user.pk)               # ProxyUser is made to add some methods (below)
    else:
        user = ProxyAnonymousUser()
    if user.tied_cart(request):                                 # this method,
        user.add_sp_to_cart(request, sp, quantity)             # this
    else:
        user.create_cart(request, sp, quantity)                # and this
    return HttpResponse()
