from django import template
register = template.Library()
from phoenix.server_settings import SITE_FULL_BASE_ADDRESS
@register.filter
def to_absolute_link(url):
    absolute_link=""
    if SITE_FULL_BASE_ADDRESS[len(SITE_FULL_BASE_ADDRESS)-1]=="/" and url[0]=="/":
        absolute_link=SITE_FULL_BASE_ADDRESS[0:len(SITE_FULL_BASE_ADDRESS)-1]+url
    else:
        absolute_link=SITE_FULL_BASE_ADDRESS+url
    return absolute_link