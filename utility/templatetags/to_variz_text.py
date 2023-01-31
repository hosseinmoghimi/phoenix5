from django import template
register = template.Library()
@register.filter
def to_variz_text(bank_account):
    if bank_account is None:
        return ""
    text=" جهت واریز : "
    if bank_account.account_no:
        text+="""<small class="text-muted"> شماره حساب : </small>"""
        text+=bank_account.account_no
    if bank_account.card_no:
        text+="""<small class="text-muted"> شماره کارت :</small> """
        text+=bank_account.card_no
    if bank_account.shaba_no:
        text+="""<small class="text-muted"> شماره شبا :</small>"""
        text+=bank_account.shaba_no
    if bank_account.account:
        text+="""<small class="text-muted"> به نام  : </small>"""
        text+= bank_account.title
    return text