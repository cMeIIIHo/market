from django import template

register = template.Library()


@register.filter
def get_range(var):
    """ returns iterable 1,2,3...,var """
    return range(1, var+1)