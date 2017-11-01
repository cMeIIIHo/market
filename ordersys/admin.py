from django.contrib import admin
from ordersys.models import *


class PickupPointAdmin(admin.ModelAdmin):
    ordering = ['closest_subway']


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    raw_id_fields = ("spec_prod",)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(PickupPoint, PickupPointAdmin)
admin.site.register(Order, OrderAdmin)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     spec_prod = models.ForeignKey(Spec_prod)
#     quantity = models.PositiveSmallIntegerField()
#     confirmed_by_price = models.FloatField(blank=True, null=True)