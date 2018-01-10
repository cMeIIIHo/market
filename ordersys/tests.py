from django.test import TestCase
from ordersys.models import *
from catalog.models import *
from django.contrib.auth.models import User
import random

few = 2
some = 5
many = 10


def create_mark(producer, brand):
    return Mark.objects.create(producer=producer, brand=brand)


def create_option_name(name, usage_in_filters, data_type):
    return Option_name.objects.create(name=name, usage_in_filters=usage_in_filters, data_type=data_type)


def create_category(name, parent_category, opt_list):
    cat_obj = Category.objects.create(name=name, parent_category=parent_category)
    cat_obj.save()
    opt_list_ids = opt_list.values_list('id', flat=True)
    cat_obj.opt_list.add(opt_list_ids)
    return cat_obj


def create_int_opt(name, value):
    return Int_opt.objects.create(name=name, value=value)


def create_text_opt(name, value):
    return Int_opt.objects.create(name=name, value=value)


def create_float_opt(name, value):
    return Int_opt.objects.create(name=name, value=value)


def create_product(category, mark, name, description):
    return Product.objects.create(category=category, mark=mark, name=name, description=description)


def create_spec_prod(product, int_opts, text_opts, float_opts, amount, price):
    sp = Spec_prod.objects.create(product=product, amount=amount, price=price)
    sp.save()
    int_opt_ids = int_opts.values_list('id', flat=True)
    text_opt_ids = text_opts.values_list('id', flat=True)
    float_opt_ids = float_opts.values_list('id', flat=True)
    sp.int_opts.add(int_opt_ids)
    sp.text_opts.add(text_opt_ids)
    sp.float_opts.add(float_opt_ids)
    return sp


class DatabaseTests(TestCase):
    fixtures = ['category.json',
                'float_opt.json',
                'int_opt.json',
                'mark.json',
                'option_name.json',
                'product.json',
                'spec_prod.json',
                'text_opt.json',
                'user.json',
                'pickup_point.json',
                'order.json',
                'order_item.json']

    @classmethod
    def setUpTestData(cls):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

    def setUp(self):
        pass

    def test_sps_created(self):
        spec_prods = Spec_prod.objects.all()
        self.assertEqual(spec_prods.count(), 12)

    def test_sp_related_to_prod(self):
        sp12 = Spec_prod.objects.get(pk=12)
        p6 = Product.objects.get(pk=6)
        self.assertTrue(sp12 in p6.spec_prod_set.all())

    def test_sps_got_opts_mentioned_in_its_category_opt_list(self):
        sps = Spec_prod.objects.all()
        for sp in sps:
            list_of_possible_option_names = sp.product.category.opt_list.all()
            sp_options = list() + list(sp.int_opts.all()) + list(sp.text_opts.all()) + list(sp.float_opts.all())
            sp_options_names = [opt.name for opt in sp_options]
            for name in sp_options_names:
                self.assertIn(name, list_of_possible_option_names)

    def test_orders_created(self):
        self.assertEqual(Order.objects.all().count(), 2)

    def test_pickup_points_created(self):
        self.assertEqual(PickupPoint.objects.all().count(), 2)

    def test_ordered_less_than_total_amount(self):
        orders = Order.objects.all()
        sps_in_all_orders = {}
        for order in orders:
            ordered_items = order.orderitem_set.all()
            for item in ordered_items:
                sp = item.spec_prod
                quantity = item.quantity
                if sp in sps_in_all_orders:
                    sps_in_all_orders[sp] += quantity
                else:
                    sps_in_all_orders[sp] = quantity
        for sp, quantity in sps_in_all_orders.items():
            self.assertTrue(quantity <= sp.amount)

    def test_at_lest_one_order_has_a_customer(self):
        orders = Order.objects.all()
        self.assertTrue(any((order.customer for order in orders)))


class OrdersysTests(TestCase):

    fixtures = ['category.json',
                'float_opt.json',
                'int_opt.json',
                'mark.json',
                'option_name.json',
                'product.json',
                'spec_prod.json',
                'text_opt.json',
                'user.json',
                'pickup_point.json',
                'order.json',
                'order_item.json']

    @classmethod
    def setUpTestData(cls):
        for user in User.objects.all():
            user.set_password(user.password)
            user.save()

    def setUp(self):
        pass
