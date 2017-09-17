from django.db import models
from django.contrib.auth.models import User, AnonymousUser
from catalog.models import Spec_prod
from django.utils import timezone


class PickupPoint(models.Model):
    address = models.TextField()
    opening_hours = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    closest_subway = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return '%s - %s' % (self.closest_subway, self.address)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    express_delivery = models.BooleanField(default=True)
    address = models.TextField(blank=True)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, blank=True, null=True)
    comment = models.TextField(blank=True)
    confirmed = models.DateField(blank=True, null=True)
    closed = models.DateField(blank=True, null=True)

    def confirm(self):
        self.confirmed = timezone.now()

    def close(self):
        self.closed = timezone.now()

    def __str__(self):
        return self.pk


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    spec_prod = models.ForeignKey(Spec_prod)
    quantity = models.PositiveSmallIntegerField()
    confirmed_by_price = models.FloatField()

    def __str__(self):
        return self.spec_prod


class ProxyUser(User):
    class Meta:
        proxy = True

    def has_cart(self, request):
        return 'cart' in request.session

    # def create_cart(self, request, sp, amount):







class ProxyAnonymousUser(AnonymousUser):
    class Meta:
        proxy = True

