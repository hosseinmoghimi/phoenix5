
from django import template
register = template.Library()

@register.filter
def to_amount_color(amount):
    if amount>0:
        return 'success'
    if amount==0:
        return 'primary'
    if amount<0:
        return 'danger'