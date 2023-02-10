from core.enums import _,TextChoices


class AttendanceStatusEnum(TextChoices):
    PRESENT="حاضر",_("حاضر")
    ABSET="غایب",_("غایب")
    DELAY="تاخیر",_("تاخیر")
    NOT_SET="ثبت نشده",_("ثبت نشده")

class SalaryTitleTypeEnum(TextChoices):
    MASKAN="حق مسکن",_("حق مسکن")
    SANAVAT="پایه سنوات",_("پایه سنوات")
    OLAD="حق اولاد",_("حق اولاد")
    OTHER="سایر",_("سایر")

class GroupTypeEnum(TextChoices):
    MANAGER="مدیر",_("مدیر")
    EMPLOYEE="کارمند",_("کارمند")
    OTHER="سایر",_("سایر")

class SalaryRowDirectionEnum(TextChoices):
    MAZAYA="مزایا",_("مزایا")
    KOSURAT="کسورات",_("کسورات")