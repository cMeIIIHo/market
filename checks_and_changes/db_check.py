import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'market.settings')

import django

django.setup()

from catalog.models import *
from django.db.models import Q


# sps = Spec_prod.objects.filter(float_opts__value=8.0).distinct()
# ps = Product.objects.filter(spec_prod__in=sps).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# ps = Product.objects.filter(spec_prod__float_opts__value=8.0).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# ps = Product.objects.filter(spec_prod__float_opts__id=188).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# fo = Float_opt.objects.filter(name__name='Радиус кривизны').filter(value=8.0)
# ps = Product.objects.filter(spec_prod__float_opts=fo).distinct()
# print(len(ps))
# for p in ps:
#     print(p)

# print(Float_opt.objects.filter(id=2.99))

# n = Product.objects.filter(spec_prod__float_opts__name__name='Радиус кривизны').distinct()
# print(len(n))

# n = Product.objects.all()
# for p in n:
#     print(p.id)



# p = Product.objects.all()
#
# p = p.filter(Q(category__name='Прозрачные линзы') |
#              Q(category__name='Цветные линзы') |
#              Q(category__name='Оттеночные линзы') |
#              Q(category__name='Карнавальные линзы') |
#              Q(category__name='Торические линзы'))
# print(len(p))
# m_list = ('Доктор Оптик', 'CooperVision')
# m = Mark.objects.filter(producer__in=m_list, brand='')
# p = p.exclude(mark__in=m)
# f_o_1 = Float_opt.objects.filter(name__name='Радиус кривизны', value=8.2)
# p = p.exclude(spec_prod__float_opts=f_o_1).distinct()
# print(len(p))
# f_o_2 = Float_opt.objects.filter(name__name='Диаметр', value=14.0)
# p = p.exclude(spec_prod__float_opts=f_o_2).distinct()
# print(len(p))
# i_o_1 = Int_opt.objects.filter(name__name='Влагосодержание', value__gte=33, value__lte=77)
# p = p.filter(spec_prod__int_opts__in=i_o_1).distinct()
# print(len(p))
# i_o_2 = Int_opt.objects.filter(name__name='DK/T', value__gte=11, value__lte=155)
# p = p.filter(spec_prod__int_opts__in=i_o_2).distinct()
# print(len(p))
# t_o = Text_opt.objects.filter(name__name='Срок замены', value='на 3 месяца')
# p = p.exclude(spec_prod__text_opts=t_o).distinct()
# print(len(p))
# -------------------------------------------------------------------------

# o = Option_name.objects.filter(data_type='')
# print(len(o))
# -------------------------------------------------------------------------

# o = Option_name.objects.all()
# print(len(o))
# o = o.values_list('name')
# print(len(o))
# o = set(o)
# print(o)
# print(len(o))
# -------------------------------------------------------------------------

# p = Product.objects.all()
#
# p = p.filter(Q(category__name='Прозрачные линзы') |
#              Q(category__name='Цветные линзы'))
# print(len(p))
#
# p = p.filter(Q(spec_prod__float_opts__value=8.3) |
#              Q(spec_prod__float_opts__value=8.7) |
#              Q(spec_prod__float_opts__value=8.6) |
#              Q(spec_prod__float_opts__value=8.8),
#              spec_prod__float_opts__name__name='Радиус кривизны').distinct()
#
#
#
# # f_o_1 = Float_opt.objects.filter(name__name='Радиус кривизны', value=8.2)
# # p = p.exclude(spec_prod__float_opts=f_o_1).distinct()
# # print(len(p))
# # f_o_2 = Float_opt.objects.filter(name__name='Диаметр', value=14.0)
# # p = p.exclude(spec_prod__float_opts=f_o_2).distinct()
# # print(len(p))
# i_o_1 = Int_opt.objects.filter(name__name='Влагосодержание', value__gte=33, value__lte=77).distinct().values_list('id')
# p = p.filter(spec_prod__int_opts__in=i_o_1).distinct()
# print(len(p))
# i_o_2 = Int_opt.objects.filter(name__name='DK/T', value__gte=22, value__lte=88).distinct().values_list('id')
# p = p.filter(spec_prod__int_opts__in=i_o_2).distinct()
# print(len(p))
# # t_o = Text_opt.objects.filter(name__name='Срок замены', value='на 3 месяца')
# # p = p.exclude(spec_prod__text_opts=t_o).distinct()
# print(len(p))
# --------------------------------------------------------------

# print(Product.objects.exclude(spec_prod__float_opts__name__name='Радиус кривизны'))
# print(Product.objects.exclude(spec_prod__float_opts__name__name='Диаметр'))

# p = Product.objects.all()
# p = p.filter(category__id__in=[2,4,6]).distinct()
# p = p.filter(mark__id__in=[1, 20, 6, 8, 10, 12, 14, 16, 18, 21, 23, 25, 27, 29, 31]).distinct()
#
# io1 = Int_opt.objects.filter(name__id=4, value__gte=11,value__lte=166).distinct()
# fo1 = Float_opt.objects.filter(id__in=(138,8,206,202)).distinct()
# io2 = Int_opt.objects.filter(name__id=3, value__gte=33,value__lte=77).distinct()
# to1 = Text_opt.objects.filter(id__in=(8,11,45)).distinct()
# fo2 = Float_opt.objects.filter(id__in=(188,1,9,2,135)).distinct()
#
# sp = Spec_prod.objects.filter(int_opts__in=io1,
#                               float_opts__in=fo1,
#                               text_opts__in=to1).filter(int_opts__in=io2, float_opts__in=fo2).values_list('product').distinct()
# p = p.filter(id__in=sp).distinct()
#
# print(len(p))
# ____________________________________________________
#
# product = Product.objects.get(name='Acuvue Oasys 6')
# sps = product.spec_prod_set.all()
# f_o = Float_opt.objects.get(name__name='Радиус кривизны', value=8.8)
# sps = sps.filter(float_opts=f_o)
# sp = sps.get(float_opts__name__name='Оптическая сила', float_opts__value=-5.75)
#
# print(product)
# print(f_o)
# print(sps)
# print(sps.count())
#
# print(sp)
# ___________________________________________________

# o = Option_name.objects.get(name='Радиус кривизны')
# print(o.text_opt_set.all())
# print(o)
#__________________________________________________

# a = json.loads('[1,2]')
# print(a)
#__________________

print(Product.objects.get(pk=444))

