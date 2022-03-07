from django.utils.translation import gettext as _
from django.db.models import TextChoices

from phoenix.settings import SITE_URL


class CurrencyEnum(TextChoices):
    TUMAN="تومان",_("تومان")
    RIAL="ریال",_("ریال")
    DOLLAR="دلار",_("دلار")



class ParameterNameEnum(TextChoices):
    VISITOR_COUNTER="تعداد بازدید",_("تعداد بازدید")
    CURRENCY="واحد پول",_("واحد پول")
    TITLE="عنوان",_("عنوان")
    FARSI_FONT_NAME="نام فونت فارسی",_("نام فونت فارسی")
    HOME_URL="لینک به خانه",_("لینک به خانه")

class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')
class UnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    GERAM="گرم",_("گرم")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    TON="تن",_("تن")
    METER="متر",_("متر")
    METER2="متر مربع",_("متر مربع")
    METER3="متر مکعب",_("متر مکعب")
    PART="قطعه",_("قطعه")
    SHAKHEH="شاخه",_("شاخه")
    DASTGAH="دستگاه",_("دستگاه")
    SERVICE="سرویس",_("سرویس")
    PACK="بسته",_("بسته")
    POCKET="کیسه",_("کیسه")
    SHOT="شات",_("شات")
    CUP="فنجان",_("فنجان")
    JOFT="جفت",_("جفت")


   
class PictureNameEnum(TextChoices):
    LOGO="لوگو",_("لوگو")
    FAVICON="آیکون",_("آیکون")
    BACKGROUND="پس زمینه",_("پس زمینه")
    
class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    ROSE = 'rose', _('rose')
    DARK = 'dark', _('dark') 
