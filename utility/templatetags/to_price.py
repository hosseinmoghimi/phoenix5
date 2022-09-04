from core.constants import CURRENCY
from core.errors import LEO_ERRORS
from django import template
from phoenix.constants import TUMAN,RIAL
register = template.Library()
from utility.currency import to_price as to_price_origin,separate as separate_origin
from utility.num import to_horuf as to_horuf_num,to_tartib as to_tartib_


@register.filter
def to_price(value,*args, **kwargs):
    return to_price_origin(value=value)

@register.filter
def to_price_rial(value):
    if CURRENCY==TUMAN:
        value=value*10
    return to_price_origin(value=value,unit=RIAL) 

 
@register.filter
def to_price_tuman(value):
    if CURRENCY==RIAL:
        value=value/10
    return to_price_origin(value=value,unit=TUMAN) 


@register.filter
def to_horuf(value):
    return to_horuf_num(value=value)

@register.filter
def to_horuf_tuman(value):
    if CURRENCY==RIAL:
        value=value/10
    return to_horuf_num(value=value)


@register.filter
def to_horuf_rial(value):
    if CURRENCY==TUMAN:
        value=value*10
    return to_horuf_num(value=value)






@register.filter
def to_price_pure(value,*args, **kwargs):
    return separate_origin(value,*args, **kwargs)

@register.filter
def separate(value,*args, **kwargs):
    return separate_origin(value,*args, **kwargs) 
    
@register.filter
def to_price_pure_rial(value):
    if CURRENCY==TUMAN:
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
