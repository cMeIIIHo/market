from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from catalog.models import Spec_prod
from ordersys.models import Order
from funcs import clean_data
from ordersys.forms import OrderForm
from django.core.exceptions import ObjectDoesNotExist


def add_sp_to_cart(request):
    """ product ajax function """
    sp_id = clean_data(request.POST.get('sp_id'), int)
    sp = get_object_or_404(Spec_prod, pk=sp_id)
    quantity = clean_data(request.POST.get('sp_quantity'), int)
    user = request.user
    if Order.is_tied_to(request.session):
        order_id = request.session['order']
        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            request.session.pop('order')
        else:
            order.add_sp(sp, quantity)
    else:
        order = Order.objects.create()
        if user.is_authenticated():
            order.customer = user
            order.save()
        order.add_sp(sp, quantity)
        order.tie(request.session)
    return HttpResponse()


def show_cart(request):
    if 'order' in request.session:
        order_id = request.session['order']
        order = Order.objects.get(pk=order_id)
        order_form = OrderForm(instance=order)
        context = {'order_form': order_form}
        return render(request, 'ordersys/cart.html', context)
    else:
        pass


# def add_sp_to_cart(request):
#     """
#     product_page ajax function
#     """
#     sp_id = clean_data(request.POST.get('sp_id'), int)
#     sp = get_object_or_404(Spec_prod, pk=sp_id)
#     quantity = clean_data(request.POST.get('sp_quantity'), int)
#     user = request.user
#     if user.is_authenticated():
#         user = ProxyUser.objects.get(pk=user.pk)               # ProxyUser is made to add some methods (below)
#     else:
#         user = ProxyAnonymousUser()
#     if user.tied_cart(request):                                 # this method,
#         user.add_sp_to_cart(request, sp, quantity)             # this
#     else:
#         user.create_cart(request, sp, quantity)                # and this
#     return HttpResponse()
#
#





    # if 'cart' not in request.session:
    #     context = {'error_header': 'Your cart is empty',
    #                'error_message': 'Before coming here,please, add something in your cart'}
    #     return render(request, USER_FRIENDLY_404, context)
    # else:
    #     order_id = request.session['cart']
    #     return render(request, USER_FRIENDLY_404, {'error_header': 'works'})
