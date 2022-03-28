from django.utils.translation import gettext as _
from django.db.models import TextChoices

 
class GuaranteeStatusEnum(TextChoices):
    VALID="معتبر",_("معتبر")
    INVALID="نامعتبر",_("نامعتبر")
    OVERED="پایان یافته",_("پایان یافته")
    IN_PROGRESS="در جریان",_("در جریان")
    CHANGED="تعویض شده",_("تعویض شده")
    REPAIRED="تعمیر شده",_("تعمیر شده")
    DENIED="برگشت داده شده",_("برگشت داده شده")
class GuaranteeTypeEnum(TextChoices):
     
    REPAIR="تعمیر",_("تعمیر")
    CHANGE="تعویض",_("تعویض")