from django.contrib import admin
from catalog.models import *

# Register your models here.

admin.site.register(Sale_card)


class OptAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            class_name = self.__class__.__name__
            opt_type = class_name.split('_')[0].lower()
            kwargs['queryset'] = Option_name.objects.filter(data_type=opt_type)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class Int_optAdmin(OptAdmin):
    pass

class Float_optAdmin(OptAdmin):
    pass

class Text_optAdmin(OptAdmin):
    pass

admin.site.register(Int_opt, Int_optAdmin)
admin.site.register(Text_opt, Text_optAdmin)
admin.site.register(Float_opt, Float_optAdmin)
admin.site.register(Category)
admin.site.register(Mark)
admin.site.register(Product)


class Option_nameAdmin(admin.ModelAdmin):
    ordering = ['name']
admin.site.register(Option_name, Option_nameAdmin)


class Spec_prodAdmin(admin.ModelAdmin):

    # specify fields to be shown on the 'list of goods' page
    # here i use models methods (f.e. get_int_opts)
    list_display = ('code', 'product', 'get_int_opts', 'get_float_opts', 'get_text_opts', 'amount', 'price')

    # separates inform into logical blocks
    fieldsets = [
        ('Товар', {'fields': ['code', 'product']}),
        ('Набор параметров', {'fields': ['int_opts', 'text_opts', 'float_opts']}),
        ('Цена, остаток', {'fields': ['amount', 'price']}),
    ]

    '''По умолчанию, поле ManyToManyField отображается как <select multiple>.
    Однако, это поле тяжело использовать при большом количестве объектов.
    Добавив ManyToManyField в этот атрибут, будет использоваться “виджет”
    с JavaScript фильтром для поиска. Смотрите описание filter_vertical
    про использование вертикального “виджета”.'''

    # remastering of ManyToManyField widget
    filter_horizontal = ['int_opts', 'float_opts', 'text_opts']

    readonly_fields = ['code']

admin.site.register(Spec_prod, Spec_prodAdmin)
