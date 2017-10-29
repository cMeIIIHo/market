from django import forms
from ordersys.models import Order, PickupPoint


class OrderForm(forms.ModelForm):
    pickup_point = forms.ModelChoiceField(queryset=PickupPoint.objects.all(), empty_label=None, widget=forms.RadioSelect(attrs={'class': 'mdl-radio__button'}))

    class Meta:
        model = Order
        fields = ['customer', 'name', 'phone', 'express_delivery', 'address', 'comment']
        widgets = {'customer': forms.HiddenInput()}


# class Order(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     name = models.CharField(max_length=50, blank=True)
#     phone = models.CharField(max_length=50, blank=True)
#     express_delivery = models.BooleanField(default=True)
#     address = models.TextField(blank=True)
#     pickup_point = models.ForeignKey(PickupPoint, on_delete=models.PROTECT, blank=True, null=True)
#     comment = models.TextField(blank=True)
#     confirmed = models.DateField(blank=True, null=True)
#     closed = models.DateField(blank=True, null=True)
