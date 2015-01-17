from django import template
register = template.Library()


@register.filter
def add_float(value, value2):
    return "{:.2f}".format(float(value) + float(value2))

@register.filter
def mul_float(value, value2):
    return "{:.2f}".format(float(value) * float(value2))

@register.filter
def after_tax(value):
    return "{:.2f}".format(float(value) * 1.14)