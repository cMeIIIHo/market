from django.db import models


class Mark(models.Model):
    producer = models.CharField(max_length=200)
    brand = models. CharField(max_length=200, blank=True)

    def __str__(self):
        if not self.brand:
            return self.producer
        else:
            return self.brand


class Option_name(models.Model):
    name = models.CharField(max_length=100, unique=True)
    usage_in_filters = models.BooleanField(default=True)
    data_type = models.CharField(max_length=20, choices=(
        ('int', 'Целое число'),
        ('float', 'Десятичная дробь'),
        ('text', 'Текст'),
    )
                                 )
    appearance_in_filters = models.CharField(max_length=70, choices=(
        ('1 col', 'значения в один столбец'),
        ('2 col', 'значения в два столбца'),
        ('interval', 'интервал от мин до макс'),
    ),                                       default='1 col')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_values(self):
        # if option_name has NO value - it returns empty QS
        if self.float_opt_set.exists():
            return self.float_opt_set.all()
        elif self.int_opt_set.exists():
            return self.int_opt_set.all()
        else:
            return self.text_opt_set.all()


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_category = models.ForeignKey('self', null=True, blank=True)
    opt_list = models.ManyToManyField(Option_name, blank=True)

    def __str__(self):
        return self.name

    def get_kids_generator(self):
        if not self.category_set.all():
            yield self
        else:
            for cat in self.category_set.all():
                for kid in cat.get_kids_generator():
                    yield kid


class Opt(models.Model):
    name = models.ForeignKey(Option_name)

    def __str__(self):
        return '%s = %s' % (self.name.name, self.value)

    class Meta:
        ordering = ['name', 'value']
        abstract = True


class Int_opt(Opt):
    value = models.IntegerField()


class Text_opt(Opt):
    value = models.TextField()


class Float_opt(Opt):
    value = models.FloatField()


class Product(models.Model):
    category = models.ForeignKey(Category, null=True, blank=True)
    mark = models.ForeignKey(Mark)
    name = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='products/', blank=True)
    banner = models.ImageField(upload_to='products/', blank=True)

    def __str__(self):
        return self.name

    def get_options(self):
        '''
        a dict with
        keys: Option_name objects
        values: Queryset of Int_opt or Float_opt or Text_opt objects
        '''
        options = {}
        spec_prods = self.spec_prod_set.filter(amount__gt=0)
        opt_names = self.category.opt_list.all()
        for opt_name in opt_names:
            opt_vals = opt_name.get_values().filter(spec_prod__in=spec_prods).distinct()
            if opt_vals.exists():
                options[opt_name] = opt_vals
        return options

    def get_choosable_options(self):
        choosable_options = {}
        for opt_name, opt_vals in self.get_options().items():
            if opt_vals.count() > 1:
                choosable_options[opt_name] = opt_vals
        return choosable_options

    def get_static_options(self):
        static_options = {}
        for opt_name, opt_vals in self.get_options().items():
            if opt_vals.count() == 1:
                static_options[opt_name] = opt_vals[0]
        return static_options


def get_code():
    try:
        return Spec_prod.objects.all().order_by('-id')[0].code + 1
    except IndexError:
        return 1001


class Spec_prod(models.Model):
    product = models.ForeignKey(Product)
    int_opts = models.ManyToManyField(Int_opt, blank=True)
    text_opts = models.ManyToManyField(Text_opt, blank=True)
    float_opts = models.ManyToManyField(Float_opt, blank=True)
    code = models.IntegerField(default=get_code)
    amount = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return '%s-%s-%s' % (self.code, self.product.category.name, self.product.name)

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

    def get_choosable_options(self):
        prod_choosable_opt_name_objs = self.product.get_choosable_options().keys()
        return [opt for opt in self.option_list() if opt.name in prod_choosable_opt_name_objs]



# only for index.html page
class Sale_card(models.Model):
    picture = models.ImageField(upload_to='sale_cards/', blank=True)
    title = models.CharField(max_length=50, blank=True)
    text = models.CharField(max_length=300, blank=True)
    category = models.ForeignKey(Category, blank=True)
    params = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title