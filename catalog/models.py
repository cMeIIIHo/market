from django.db import models
# from django.utils.encoding import  import python_2_unicode_compatible
import datetime
from django.utils import timezone

class Mark(models.Model):
    producer = models.CharField(max_length=200)
    brand = models. CharField(max_length=200, blank=True)

    def __str__(self):
        if not self.brand:
            return self.producer
        else:
            return self.brand


class Option_name(models.Model):
    name = models.CharField(max_length=100)
    usage_in_filters = models.BooleanField(default=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    opt_list = models.ManyToManyField(Option_name, blank=True)

    def __str__(self):
        return self.name

class Int_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.IntegerField()
    active_in = models.ManyToManyField(Category, blank=True)


    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

class Text_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.TextField()
    active_in = models.ManyToManyField(Category, blank=True)


    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

class Float_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.FloatField()
    active_in = models.ManyToManyField(Category, blank=True)


    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True)
    mark = models.ForeignKey(Mark)
    name = models.CharField(max_length=100)
    description = models.TextField()
    pictute = models.ImageField(upload_to='products/', blank=True)
    banner = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name


def get_code():
    try:
        return Spec_prod.objects.all().order_by('-id')[0].code+1
    except IndexError:
        return 1001


    # try:
    #     return Spec_prod.objects.all()[-1].id + 2000
    # except AssertionError:
    #     return 1001

class Spec_prod(models.Model):
    product = models.ForeignKey(Product)
    int_opts = models.ManyToManyField(Int_opt, blank=True)
    text_opts = models.ManyToManyField(Text_opt, blank=True)
    float_opts = models.ManyToManyField(Float_opt, blank=True)
    code = models.IntegerField(default=get_code)
    amount = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return '%s-%s-%s' % (self.code, self.product.name, self.product.name)

    def get_int_opts(self):
        return '; '.join([str(obj) for obj in self.int_opts.all()])

    def get_float_opts(self):
        return '; '.join([str(obj) for obj in self.float_opts.all()])

    def get_text_opts(self):
        return '; '.join([str(obj) for obj in self.text_opts.all()])

    def option_list(self):
        opt_list = []
        opt_list.extend(list(self.int_opts.all()))
        opt_list.extend(list(self.text_opts.all()))
        opt_list.extend(list(self.float_opts.all()))
        return opt_list

    # def save(self):
    #     super().save()
    #     if self.amount > 0:
    #         for opt in self.option_list:
    #             if self.product.category not in opt.active_in.all():
    #                 opt.active_in.add(self.product.category)
    #     else:
    #         for opt in self.option_list:


class Sale_card(models.Model):
    picture = models.ImageField(upload_to='sale_cards/', blank=True)
    title = models.CharField(max_length=50, blank=True)
    text = models.CharField(max_length=300, blank=True)
    link = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title





# class Question(models.Model):
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField("date published")
#
#     def __str__(self):
#         return self.question_text
#
#     def was_published_recently(self):
#         now = timezone.now()
#         return now - datetime.timedelta(days=1) <= self.pub_date <= now
#
#     was_published_recently.admin_order_field = 'pub_date'
#     was_published_recently.boolean = True
#     was_published_recently.short_description = 'Published recently?'
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
#     def __str__(self):
#         return self.choice_text