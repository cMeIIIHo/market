from django.db import models
from django.contrib.auth.models import User
from catalog.models import Spec_prod
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from phonenumber_field.modelfields import PhoneNumberField
from django.http import Http404
from django.core.exceptions import ValidationError


def validate_positive(value):
    if value <= 0:
        raise ValidationError('this number must be positive')


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

    def is_empty(self):
        return not self.orderitem_set.exists()

    def remove_item(self, order_item_id):
        try:
            order_item = self.orderitem_set.get(pk=order_item_id)
        except ObjectDoesNotExist:
            raise Http404("there is no orderitem with id '%s' in order with id '%s'" % (order_item_id, self.id))
        order_item.delete()

    def tie(self, session):
        session['order'] = self.id

    def untie(self, session):
        if self.is_tied_to(session):
            session.pop('order')

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
    quantity = models.PositiveSmallIntegerField(verbose_name="количество", validators=[validate_positive])
    confirmed_by_price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.spec_prod)
