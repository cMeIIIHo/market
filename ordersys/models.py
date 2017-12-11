from django.db import models
from django.contrib.auth.models import User
from catalog.models import Spec_prod
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.modelfields import PhoneNumberField
from django.http import Http404
import funcs


class PickupPoint(models.Model):
    address = models.TextField()
    opening_hours = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    closest_subway = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return '%s - %s' % (self.closest_subway, self.address)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, verbose_name='имя, Фамилия')
    phone = PhoneNumberField(blank=True, verbose_name="телефон")
    express_delivery = models.BooleanField(default=True, verbose_name="курьерская доставка")
    address = models.CharField(max_length=100, blank=True, verbose_name="адрес доставки")
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, blank=True, null=True, verbose_name="пункт самовывоза")
    comment = models.TextField(blank=True, verbose_name="комментарии к заказу")
    confirmed = models.DateField(blank=True, null=True)
    closed = models.DateField(blank=True, null=True)

    def confirm(self, session):
        self.confirmed = timezone.now()
        self.untie(session)

    def close(self):
        self.closed = timezone.now()

    def __str__(self):
        return str(self.pk)

    def add_sp(self, sp, quantity):
        order_item, created = self.orderitem_set.get_or_create(spec_prod=sp, defaults={'quantity': quantity})
        if not created:
            order_item.quantity += quantity
            order_item.save()

    def remove_ordered_item(self, oi_id):
        try:
            oi = self.orderitem_set.get(id=oi_id)
        except ObjectDoesNotExist:
            funcs.signal('attempt of deleting nonexistent order_item (id: %s) from order (id: %s)' % (oi_id, self.id))
            raise Http404
        oi.delete()
        if self.orderitem_set.count() == 0:
            self.delete()

    def tie(self, session):
        session['order'] = self.id

    def untie(self, session):
        if not session.pop('order', default=False):
            funcs.signal('Untying from session alrdy untied order. User id: %s' % session.user.id)

    @staticmethod
    def is_tied_to(session):
        return 'order' in session

    @classmethod
    def synchronize(cls, user, session):
        """
        when user is registering or is logging in,
        we should check and synchronize order's data, stored in session and database:
        """
        if cls.is_tied_to(session):                             # if there is order data (id) in session
            order_id = session['order']                         # get it
            if cls.objects.filter(customer=user).exists():      # and if user has order data in DB
                cls.objects.filter(customer=user).delete()      # delete it
            try:
                order = cls.objects.get(pk=order_id)            # get order object depending on data from session
            except ObjectDoesNotExist:                          # in case it exists
                session.pop('order')                            # otherwise delete order data (id) from session
            else:                                               # if we got order object
                order.customer = user                           # set that order object's customer attr as current user
                order.save()
        elif cls.objects.filter(customer=user).exists():        # if ther eis NO order data (id) in session, but in DB
            order = cls.objects.filter(customer=user).last()    # get and order object
            order.tie(session)                                  # and store its data (id) into the session


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    spec_prod = models.ForeignKey(Spec_prod, on_delete=models.PROTECT)
    # todo: max_length of SP quantity
    quantity = models.PositiveSmallIntegerField(verbose_name="количество")
    confirmed_by_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.spec_prod)


# class ProxyUser(User):
#     class Meta:
#         proxy = True
#
#     @staticmethod
#     def tied_cart(request):
#         return request.session.get('cart', False)
#
#     def create_cart(self, request, sp, quantity):
#         order = Order.objects.create(customer=self)
#         OrderItem.objects.create(order=order, spec_prod=sp, quantity=quantity)
#         request.session['cart'] = order.id
#
#     def has_cart(self):
#         return self.order_set.filter(closed=None).exists()
#
#     @property
#     def cart(self):
#         return self.order_set.filter(closed=None).last()
#
#     @staticmethod
#     def add_sp_to_cart(request, sp, quantity):
#         print('\n', '1', '\n')
#         order_id = request.session['cart']
#         order = get_object_or_404(Order, pk=order_id)
#         order_item, created = order.orderitem_set.get_or_create(spec_prod=sp, defaults={'quantity': quantity})
#         if not created:
#             print('\n', '2', '\n')
#             order_item.quantity += quantity
#             order_item.save()
#
#         # order_id = request.session['cart']
#         # OrderItem.objects.create(order_id=order_id, spec_prod=sp, quantity=quantity)
#
#     def sign_tied_cart(self, order_id):
#         cart = Order.objects.get(id=order_id)
#         cart.customer = self
#         cart.save()
#
#     def synchronize_cart(self, request):
#         if self.tied_cart(request):
#             order_id = self.tied_cart(request)
#             if self.has_cart():
#                 self.cart.delete()                                      # deleting an 'old' cart from previous session
#             self.sign_tied_cart(order_id)                               # defines cart object's 'customer' attribute
#         elif self.has_cart():
#             request.session['cart'] = self.cart.id
#
#
# class ProxyAnonymousUser(AnonymousUser):
#     class Meta:
#         proxy = True
#
#     @staticmethod
#     def tied_cart(request):
#         return 'cart' in request.session
#
#     @staticmethod
#     def create_cart(request, sp, quantity):
#         order = Order.objects.create()
#         OrderItem.objects.create(order=order, spec_prod=sp, quantity=quantity)
#         request.session['cart'] = order.id
#
#     @staticmethod
#     def add_sp_to_cart(request, sp, quantity):
#         order_id = request.session['cart']
#         order = get_object_or_404(Order, pk=order_id)
#         order_item, created = order.orderitem_set.get_or_create(spec_prod=sp, defaults={'quantity': quantity})
#         if not created:
#             order_item.quantity += quantity
#             order_item.save()
#
#         # order_id = request.session['cart']
#         # OrderItem.objects.create(order_id=order_id, spec_prod=sp, quantity=quantity)

