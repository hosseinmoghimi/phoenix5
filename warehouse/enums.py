from django.utils.translation import gettext as _
from django.db.models import TextChoices

class WareHouseSheetStatusEnum(TextChoices):
    INITIAL="تعریف اولیه",_("تعریف اولیه")
    IN_PROGRESS="در جریان",_("در جریان")
    DONE="تمام شده",_("تمام شده") 
class WareHouseSheetDirectionEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار") 