from core.enums import _,TextChoices

SalaryRows=[
    'بیمه عمر سهم کارمند',
    'بیمه تامین اجتماعی سهم کارمند',
    'يمه بازنشستگي سهم كارمند',
    'بيمه تكميلي',
 
    'مزایای شغلی مستمر',
    'مزایای شغلی فوق‌العاده',
    'حقوق  پایه',
    ' اضافه کار',
    'کار در شب و کشیک فوق‌العاده',
    'حضور در جلسات',
    'کمک هزینه مسکن',
    'کمک هزینه اولاد',
    'کمک هزینه ایاب و ذهاب',
    'کمک هزینه خوراک',
    'پاداش مستمر',
    'دستمزد کارآموزی',
    'عیدی',
    'پاداش های مربوط به افزایش تولید',
    'مالیات',
]
class CrossTypeEnum(TextChoices):
    ENTER="ورود",_("ورود")
    ENTER_HOURLY="ورود ساعتی",_("ورود ساعتی")
    EXIT="خروج",_("خروج")
    EXIT_HOURLY="خروج ساعتی",_("خروج ساعتی")
    INVALID="غیر معتبر",_("غیر معتبر")
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