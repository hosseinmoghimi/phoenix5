from django.utils.translation import gettext as _
from django.db.models import TextChoices

class WareHouseSheetStatusEnum(TextChoices):
    INITIAL="پیش نویس",_("پیش نویس")
    IN_PROGRESS="در جریان",_("در جریان")
    DONE="تایید شده",_("تایید شده") 
class WareHouseSheetDirectionEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار") 