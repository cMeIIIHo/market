from django.contrib import admin
from ordersys.models import *


class PickupPointAdmin(admin.ModelAdmin):
    ordering = ['closest_subway']

admin.site.register(PickupPoint, PickupPointAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
