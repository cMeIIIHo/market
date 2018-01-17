from django.test import TestCase
from ordersys.models import *
from catalog.models import *
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from funcs import turn_integer

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


class LoginsysTests(TestCase):
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

    def test_user_can_be_logged_in(self):
        client = self.client
        data = {'username': 'user1', 'password': 'password1'}
        response = client.post(reverse('loginsys:user_login'), data)  # login our client
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated())                      # check user exists
        self.assertEqual(user, User.objects.get(username='user1'))    # check that user is logged

    def test_after_user_login_cart_gets_its_customer(self):
        client = self.client
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)
        data = {'username': 'user1', 'password': 'password1'}
        response = client.post(reverse('loginsys:user_login'), data)    # login our user
        user = response.wsgi_request.user
        self.assertEqual(user, User.objects.get(username='user1'))      # check that user is logged
        order_id = turn_integer(client.session['order'])
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.customer, user)

    def test_after_user_logout_cart_remains(self):
        client = self.client
        data = {'username': 'user1', 'password': 'password1'}
        response = client.post(reverse('loginsys:user_login'), data)  # login our user
        user = response.wsgi_request.user
        self.assertEqual(user, User.objects.get(username='user1'))    # check that user is logged
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)         # add some to the cart
        order_id = turn_integer(client.session['order'])
        response = client.get(reverse('loginsys:user_logout'))        # logout user
        order = Order.objects.get(pk=order_id)
        self.assertTrue(response.wsgi_request.user, None)   # user is logged out
        self.assertTrue(order)                              # but his order still exists
        self.assertEqual(order.customer, user)              # and user marked as a customer in it
        self.assertFalse(Order.is_tied_to(client.session))

    def test_if_user_login_he_gets_his_old_cart_if_exists(self):
        client = self.client
        data = {'username': 'user1', 'password': 'password1'}
        client.post(reverse('loginsys:user_login'), data)           # login our user
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)       # add some to the cart
        client.get(reverse('loginsys:user_logout'))                 # logout user
        self.assertFalse(Order.is_tied_to(client.session))
        data = {'username': 'user1', 'password': 'password1'}
        client.post(reverse('loginsys:user_login'), data)           # login our user
        self.assertTrue(Order.is_tied_to(client.session))
        order_id = client.session['order']
        order = Order.objects.get(pk=order_id)
        self.assertEqual(order.customer.username, 'user1')
        self.assertEqual(order.orderitem_set.get().quantity, 2)
        self.assertEqual(order.orderitem_set.get().spec_prod.id, 4)

    def test_after_user_login_his_new_cart_overrides_old_one(self):
        client = self.client
        data = {'username': 'user1', 'password': 'password1'}
        client.post(reverse('loginsys:user_login'), data)           # login our user
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)       # add some to the cart
        old_order_id = turn_integer(client.session['order'])
        client.get(reverse('loginsys:user_logout'))                 # logout user
        data = {'sp_id': '5', 'sp_quantity': '1'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)       # add some to the cart
        data = {'username': 'user1', 'password': 'password1'}
        client.post(reverse('loginsys:user_login'), data)           # login our user
        new_order_id = turn_integer(client.session['order'])
        self.assertFalse(old_order_id is new_order_id)
        self.assertTrue(Order.exists(pk=new_order_id))
        self.assertFalse(Order.exists(pk=old_order_id))


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

    def test_anonymous_can_add_item_to_an_empty_cart(self):
        client = self.client
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)
        self.assertTrue(Order.is_tied_to(client.session))
        order_id = turn_integer(client.session['order'])
        order = Order.objects.get(pk=order_id)
        self.assertTrue(order)
        self.assertFalse(order.is_empty())
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertTrue(order.orderitem_set.get())
        self.assertEqual(order.orderitem_set.get().spec_prod.id, 4)
        self.assertEqual(order.orderitem_set.get().quantity, 2)
        self.assertTrue(order.customer is None)

    def test_anonymous_can_add_item_to_existing_cart(self):
        client = self.client
        data = {'sp_id': '4', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)   # add first item
        data = {'sp_id': '5', 'sp_quantity': '1'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)   # add second item
        order_id = turn_integer(client.session['order'])
        order = Order.objects.get(pk=order_id)                  # find created order
        self.assertTrue(order)
        self.assertFalse(order.is_empty())
        self.assertEqual(order.orderitem_set.count(), 2)
        self.assertTrue(order.orderitem_set.get(spec_prod_id=5, quantity=1))    # both items
        self.assertTrue(order.orderitem_set.get(spec_prod_id=4, quantity=2))    # in the order
        self.assertTrue(order.customer is None)
        self.assertTrue(order.is_tied_to(client.session))

    def test_sp_with_negative_quantity_cant_be_added_to_an_empty_cart(self):
        client = self.client
        data = {'sp_id': '4', 'sp_quantity': '-2'}
        response = client.post(reverse('ordersys:add_sp_to_cart'), data)
        self.assertEqual(response.status_code, 404)                             # ajax gets 404 page
        self.assertFalse(Order.objects.filter(orderitem__quantity=-2).exists())
        self.assertFalse(OrderItem.objects.filter(quantity=-2).exists())
        self.assertFalse(Order.is_tied_to(client.session))

    def test_sp_with_zero_quantity_cant_be_added_to_an_empty_cart(self):
        client = self.client
        data = {'sp_id': '4', 'sp_quantity': '0'}
        response = client.post(reverse('ordersys:add_sp_to_cart'), data)
        self.assertEqual(response.status_code, 404)                             # ajax gets 404 page
        self.assertFalse(Order.objects.filter(orderitem__quantity=0).exists())
        self.assertFalse(OrderItem.objects.filter(quantity=0).exists())
        self.assertFalse(Order.is_tied_to(client.session))

    def test_sp_with_negative_quantity_cant_be_added_to_the_existing_cart(self):
        client = self.client
        data = {'sp_id': '6', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)
        data = {'sp_id': '5', 'sp_quantity': '-1'}
        response = client.post(reverse('ordersys:add_sp_to_cart'), data)
        self.assertEqual(response.status_code, 404)                             # ajax gets 404 page
        self.assertFalse(Order.objects.filter(orderitem__quantity=-1).exists())
        self.assertFalse(OrderItem.objects.filter(quantity=-1).exists())
        self.assertTrue(Order.is_tied_to(client.session))
        order_id = turn_integer(client.session['order'])
        order = Order.objects.get(pk=order_id)                                  # find created order
        self.assertTrue(order)
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertTrue(order.orderitem_set.get(spec_prod_id=6, quantity=2))    # only first item in the order

    def test_sp_with_zero_quantity_cant_be_added_to_the_existing_cart(self):
        client = self.client
        data = {'sp_id': '6', 'sp_quantity': '2'}
        client.post(reverse('ordersys:add_sp_to_cart'), data)
        data = {'sp_id': '5', 'sp_quantity': '0'}
        response = client.post(reverse('ordersys:add_sp_to_cart'), data)
        self.assertEqual(response.status_code, 404)                             # ajax gets 404 page
        self.assertFalse(Order.objects.filter(orderitem__quantity=-1).exists())
        self.assertFalse(OrderItem.objects.filter(quantity=0).exists())
        self.assertTrue(Order.is_tied_to(client.session))
        order_id = turn_integer(client.session['order'])
        order = Order.objects.get(pk=order_id)                                  # find created order
        self.assertTrue(order)
        self.assertEqual(order.orderitem_set.count(), 1)
        self.assertTrue(order.orderitem_set.get(spec_prod_id=6, quantity=2))    # only first item in the order
