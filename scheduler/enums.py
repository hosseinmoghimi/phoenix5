from core.enums import _,TextChoices

class AppointmentStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    APPROVED="تایید شده",_("تایید شده")
    DONE="انجام شده",_("انجام شده")
    CANCELED="کنسل شده",_("کنسل شده")