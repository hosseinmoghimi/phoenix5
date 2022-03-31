from core.enums import CurrencyEnum
from core.errors import LEO_ERRORS
from django import template
register = template.Library()
from utility.currency import to_price as to_price_origin
from utility.num import to_horuf as to_horuf_num,to_tartib as to_tartib_


@register.filter
def to_price(value,*args, **kwargs):
    return to_price_origin(value=value)

@register.filter
def to_price_rial(value):
    value=value*10
    return to_price_origin(value=value,unit=CurrencyEnum.RIAL) 

 

@register.filter
def to_horuf(value):
    return to_horuf_num(value=value)


@register.filter
def to_horuf_rial(value):
    value=value*10
    return to_horuf_num(value=value)






@register.filter
def to_price_pure(value):
    """converts int to string"""  
    try:
        sign=''
        if value<0:
            value=0-value
            sign='- '
        a=separate(value)
        return sign+a
    except:
        # return LEO_ERRORS.error_to_price_template_tag
        return ""



@register.filter
def to_price_pure_rial(value):
    value=value*10
    return to_price_pure(value=value)
    





 
 


@register.filter
def to_tartib(value):
    return to_tartib_(value)


def separate(value):
    try:
        value=int(value)
    except:
        # return LEO_ERRORS.error_to_price_template_tag
        return ""

    if value<0:
        return '-'+separate(value=0-value)
    
    if value<1000:
        return str(value)
    else:
        return separate(value/1000)+','+str(value)[-3:]
