from django.contrib import admin
from catalog.models import *

# Register your models here.

admin.site.register(Sale_card)
class Int_optAdmin(admin.ModelAdmin):
    pass
    # ordering = ['name']



admin.site.register(Int_opt, Int_optAdmin)
admin.site.register(Text_opt)
admin.site.register(Float_opt)
admin.site.register(Mark)

class Option_name_Admin(admin.ModelAdmin):
    ordering = ['name']
admin.site.register(Option_name, Option_name_Admin)
admin.site.register(Product)

class Spec_prodAdmin(admin.ModelAdmin):

    # specify fields to be shown on the 'list of goods' page
    #here i use models methods (f.e. get_int_opts)
    list_display = ('code', 'product', 'get_int_opts', 'get_float_opts', 'get_text_opts', 'amount', 'price')

    # separates inform into logical blocks
    fieldsets = [
        ('Товар', {'fields':['code', 'product']}),
        ('Набор параметров', {'fields':['int_opts', 'text_opts', 'float_opts']}),
        ('Цена, остаток', {'fields':['amount', 'price']}),
    ]

    '''По умолчанию, поле ManyToManyField отображается как <select multiple>.
    Однако, это поле тяжело использовать при большом количестве объектов.
    Добавив ManyToManyField в этот атрибут, будет использоваться “виджет”
    с JavaScript фильтром для поиска. Смотрите описание filter_vertical
    про использование вертикального “виджета”.'''

    #remastering of ManyToManyField widget
    filter_horizontal = ['int_opts', 'float_opts', 'text_opts']

    readonly_fields = ['code']

admin.site.register(Spec_prod, Spec_prodAdmin)



# class Mark(models.Model):
#     producer = models.CharField(max_length=200)
#     brand = models. CharField(max_length=200, blank=True)
#
#     def __str__(self):
#         return self.brand
#
#
# class Option_name(models.Model):
#     name = models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.name
#
# class Int_opt(models.Model):
#     name = models.ForeignKey(Option_name)
#     value = models.IntegerField()
#
#     def __str__(self):
#         return self.name
#
# class Text_opt(models.Model):
#     name = models.ForeignKey(Option_name)
#     value = models.TextField()
#
#     def __str__(self):
#         return self.name
#
# class Sub_type(models.Model):
#     name = models.CharField(max_length=100)
#     opt_list = models.ManyToManyField(Option_name)
#
#     def __str__(self):
#         return self.name
#
# class Prod_type(models.Model):
#     name = models.CharField(max_length=100)
#     sub_type_list = models.ManyToManyField(Sub_type)
#
#     def __str__(self):
#         return self.name
#
# class Product(models.Model):
#     prod_type = models.ForeignKey(Prod_type)
#     sub_type = models.ForeignKey(Sub_type)
#     mark = models.ForeignKey(Mark)
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.name
#
# class Spec_prod(models.Model):
#     product = models.ForeignKey(Product)
#     int_opts = models.ManyToManyField(Int_opt)
#     text_opts = models.ManyToManyField(Text_opt)
#     code = models.IntegerField()
#     amount = models.IntegerField()
#     price = models.FloatField()
#
#     def __str__(self):
#         return self.code