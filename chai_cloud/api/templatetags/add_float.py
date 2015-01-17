from django import template
register = template.Library()


@register.filter
def add_float(value, value2):
    return "{:.2f}".format(float(value) + float(value2))
