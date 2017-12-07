from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from catalog.models import Spec_prod
from ordersys.models import Order, OrderItem
from funcs import clean_data
from ordersys.forms import OrderForm, OrderItemForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.forms import inlineformset_factory
from django import forms


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
    OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0)
    session = request.session
    if Order.is_tied_to(session):                                                               # getting Order object
        order_id = session['order']
        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            session.pop('order')
            raise Http404('This order does not exist')
    else:
        raise Http404('Your cart is empty')

    if request.method == 'GET':                                                                  # GET method logic
        order_form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
        return render(request, 'ordersys/cart.html', {'order_form': order_form,
                                                      'formset': formset,})

    elif request.method == 'POST':                                                              # POST method logic
        filled_form = OrderForm(request.POST, instance=order)
        filled_formset = OrderItemFormSet(request.POST, instance=order)
        if filled_form.is_valid() and filled_formset.is_valid():
            order = filled_form.save(commit=False)
            order.confirm()
            order.save()
            filled_formset.save()
            return redirect('catalog:index')
        else:
            return render(request, 'ordersys/cart.html', {'order_form': filled_form,
                                                          'formset': filled_formset,})

# def show_cart(request):
#     OrderItemFormSet = inlineformset_factory(Order, OrderItem, fields=('spec_prod', 'quantity'), extra=0,
#                                              widgets={'spec_prod': forms.TextInput()})
#     session = request.session
#     if Order.is_tied_to(session):  # getting Order object
#         order_id = session['order']
#         try:
#             order = Order.objects.get(pk=order_id)
#         except ObjectDoesNotExist:
#             session.pop('order')
#             raise Http404('This order does not exist')
#     else:
#         raise Http404('Your cart is empty')
#
#     if request.method == 'GET':  # GET method logic
#         order_form = OrderForm(instance=order)
#         formset = OrderItemFormSet(instance=order)
#         return render(request, 'ordersys/cart.html', {'order_form': order_form, 'formset': formset})
#
#     elif request.method == 'POST':  # POST method logic
#         filled_form = OrderForm(request.POST, instance=order)
#         if filled_form.is_valid():
#             order = filled_form.save()
#             order.confirm()
#             order.save()
#             return redirect('catalog:index')
#         else:
#             return render(request, 'ordersys/cart.html', {'order_form': filled_form})







    # if 'order' in request.session:
    #     order_id = request.session['order']
    #     order = Order.objects.get(pk=order_id)
    #     order_form = OrderForm(instance=order)
    #     context = {'form': order_form}
    #     return render(request, 'ordersys/cart.html', context)
    # else:
    #     pass


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
