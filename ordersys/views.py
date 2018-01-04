from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from catalog.models import Spec_prod
from ordersys.models import Order, OrderItem
from funcs import clean_data, turn_integer, check_positive
from ordersys.forms import OrderForm, OrderItemForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.forms import inlineformset_factory
from market.settings import INFORM_USER


def add_sp_to_cart(request):
    """ product ajax function """
    sp_id = check_positive(turn_integer(request.POST.get('sp_id', 'empty')))
    sp = get_object_or_404(Spec_prod, pk=sp_id)
    quantity = check_positive(turn_integer(request.POST.get('sp_quantity', 'empty')))
    user = request.user
    if Order.is_tied_to(request.session):
        order_id = request.session['order']
        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            request.session.pop('order')
            raise Http404('session contains order_id "%s", but order does not exist' % order_id)
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
    OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=0, can_delete=True)
    session = request.session
    if Order.is_tied_to(session):                                                               # getting Order object
        order_id = session['order']
        try:
            order = Order.objects.get(pk=order_id)
        except ObjectDoesNotExist:
            session.pop('order')
            raise Http404('This order does not exist')
    else:
        return render(request, INFORM_USER, {'header': 'Your cart is empty',
                                             'message': 'No time to explain. GO and buy something'})

    if request.method == 'GET':                                                                  # GET method logic
        order_form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
        return render(request, 'ordersys/cart.html', {'order_form': order_form,
                                                      'formset': formset})

    elif request.method == 'POST':                                                              # POST method logic
        # for key, value in request.POST.lists():
        #     print(key, ': ', value)
        filled_form = OrderForm(request.POST, instance=order)
        filled_formset = OrderItemFormSet(request.POST, instance=order)
        if filled_form.is_valid() and filled_formset.is_valid():
            order = filled_form.save(commit=False)
            order.confirm(session)
            order.save()
            # todo: what if user will set amount of ordered SP equal to ZERO ? - we should del this position (?)
            filled_formset.save()
            return redirect('catalog:index')
        else:
            return render(request, 'ordersys/cart.html', {'order_form': filled_form,
                                                          'formset': filled_formset})


def delete_order_item(request):
    order_id = clean_data(request.POST['order_id'], int)
    item_id = clean_data(request.POST['item_id'], int)
    order = get_object_or_404(Order, pk=order_id)
    order.remove_item(item_id)
    if order.is_empty():
        order.untie(request.session)
        order.delete()
    return HttpResponse()








    # try:
    #     order = Order.objects.get(pk=order_id)
    # except ObjectDoesNotExist:
    #     funcs.signal('some1 is trying to delete item from nonexistent order(id=%s)' % order_id)
    #     raise Http404
    # try:
    #     item = order.orderitem_set.get(pk=item_id)
    # except ObjectDoesNotExist:
    #     funcs.signal('attempt of removing from the cart unexistent item or item that is not tied to taht order (order_id=%s, item_id=%s)' % (order_id, item_id))
    #     raise Http404
    # item.delete()
    # return HttpResponse()

