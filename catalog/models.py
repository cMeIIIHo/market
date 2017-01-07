from django.db import models
# from django.utils.encoding import  import python_2_unicode_compatible
import datetime
from django.utils import timezone

class Mark(models.Model):
    producer = models.CharField(max_length=200)
    brand = models. CharField(max_length=200, blank=True)

    def __str__(self):
        return self.brand


class Option_name(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Int_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.IntegerField()

    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

class Text_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.TextField()

    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

class Float_opt(models.Model):
    name = models.ForeignKey(Option_name)
    value = models.FloatField()

    class Meta:
        ordering = ['name', 'value']

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

class Sub_type(models.Model):
    name = models.CharField(max_length=100)
    opt_list = models.ManyToManyField(Option_name)

    def __str__(self):
        return self.name

class Prod_type(models.Model):
    name = models.CharField(max_length=100)
    sub_type_list = models.ManyToManyField(Sub_type, blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    prod_type = models.ForeignKey(Prod_type)
    sub_type = models.ForeignKey(Sub_type, blank=True)
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
        return '%s-%s-%s' % (self.code, self.product.prod_type.name, self.product.name)





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