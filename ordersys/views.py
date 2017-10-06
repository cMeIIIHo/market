from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from ordersys.models import ProxyUser, ProxyAnonymousUser
from catalog.models import Spec_prod
from ordersys.models import Order
from funcs import clean_data
from market.settings import USER_FRIENDLY_404
from funcs import clean_data
from ordersys.forms import CartForm


def add_sp_to_cart(request):
    """ product ajax function """
    sp_id = clean_data(request.POST.get('sp_id'), int)
    sp = get_object_or_404(Spec_prod, pk=sp_id)
    quantity = clean_data(request.POST.get('sp_quantity'), int)
    user = request.user
    if 'cart' in request.session:
        pass
    else:
        cart = Order().create_cart(user, sp, quantity)
        cart.tie(request.session)


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
# def show_cart(request):
#     if 'cart' in request.session:
#         order_id = request.session['cart']
#         cart = Order.objects.get(pk=order_id)
#         cart_form = CartForm(instance=cart)
#         context = {'cart_form': cart_form}
#         return render(request, 'ordersys/cart.html', context)
#     else:
#         pass




    # if 'cart' not in request.session:
    #     context = {'error_header': 'Your cart is empty',
    #                'error_message': 'Before coming here,please, add something in your cart'}
    #     return render(request, USER_FRIENDLY_404, context)
    # else:
    #     order_id = request.session['cart']
    #     return render(request, USER_FRIENDLY_404, {'error_header': 'works'})
