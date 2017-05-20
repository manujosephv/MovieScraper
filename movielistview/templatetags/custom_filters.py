from django import template

register = template.Library()

@register.filter(name='get_no_of_stars')
def get_no_of_stars(value):
    if value is None:
        return 0
    else:
        return (round(float(value)/float(2)))