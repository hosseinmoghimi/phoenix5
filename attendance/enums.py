from core.enums import _,TextChoices


class AttendanceStatusEnum(TextChoices):
    PRESENT="حاضر",_("حاضر")
    ABSET="غایب",_("غایب")
    DELAY="تاخیر",_("تاخیر")
    NOT_SET="ثبت نشده",_("ثبت نشده")