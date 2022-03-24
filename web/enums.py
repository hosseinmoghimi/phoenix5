from django.db.models import TextChoices
from django.utils.translation import gettext as _


class ParameterNameEnum(TextChoices):
    OFFICE_ADDRESS="آدرس دفتر",_("آدرس دفتر")
    OFFICE_TEL="تلفن دفتر",_("تلفن دفتر")
    OFFICE_EMAIL="ایمیل دفتر",_("ایمیل دفتر")
    OFFICE_MOBILE="شماره همراه",_("شماره همراه")