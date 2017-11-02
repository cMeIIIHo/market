from django import forms
from ordersys.models import Order, PickupPoint
from phonenumber_field.formfields import PhoneNumberField


class OrderForm(forms.ModelForm):
    name = forms.CharField(max_length=50, required=True,
                           widget=forms.TextInput(attrs={'placeholder': 'example: Naumov Vitaly'}))
    phone = PhoneNumberField(max_length=50, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'example: +79110254614', 'type': 'tel'}),
                             error_messages={'invalid': 'Please, enter valid number, example: +79110254614'})
    address = forms.CharField(max_length=100, required=False,
                              widget=forms.TextInput(attrs={'placeholder': 'example: SPB, Vernosti 28'}))
    pickup_point = forms.ModelChoiceField(queryset=PickupPoint.objects.filter(is_active=True),
                                          empty_label=None,
                                          required=False,
                                          widget=forms.RadioSelect(attrs={'class': 'mdl-radio__button'}))

    class Meta:
        model = Order
        fields = ['name', 'phone', 'express_delivery', 'address', 'comment', 'pickup_point']

    def clean(self):
        cleaned_data = super(forms.ModelForm, self).clean()
        express_delivery = cleaned_data.get('express_delivery')
        address = cleaned_data.get('address')
        pickup_point = cleaned_data.get('pickup_point')
        if express_delivery and pickup_point:
            raise forms.ValidationError('U should chose either EXPRESS_DELIVERY or PICKUP_POINT')
        if express_delivery and not address:
            self.add_error('address', 'Please, specify delivery address')
        if pickup_point and address:
            self.add_error('address', "You've specified your address, but also u chose PICKUP_POINT")
        if not express_delivery and not pickup_point:
            raise forms.ValidationError('Please specify delivery conditions')






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
