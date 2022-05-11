from django.utils.translation import gettext as _
from django.db.models import TextChoices

from phoenix.settings import SITE_URL

class AppNameEnum(TextChoices):
    projectmanager='projectmanager',_('projectmanager')
    accounting='accounting',_('accounting')
    web='web',_('web')
    transport='transport',_('transport')
    log='log',_('log')
    map='map',_('map')
    market='market',_('market')
    stock='stock',_('stock')
    authentication='authentication',_('authentication')
    dashboard='dashboard',_('dashboard')

class CurrencyEnum(TextChoices):
    TUMAN="تومان",_("تومان")
    RIAL="ریال",_("ریال")
    DOLLAR="دلار",_("دلار")


def class_title(*args, **kwargs):
    class_name='page'
    app_name='core'
    if 'class_name' in kwargs:
        class_name=kwargs['class_name']
    if 'app_name' in kwargs:
        app_name=kwargs['app_name']

    class_title = "صفحه"
    if class_name == "page":
        class_title = "صفحه"
    elif class_name == "appointment":
        class_title = "قرار ملاقات"
    elif class_name == "letter":
        class_title = "نامه"
    elif class_name == "file":
        class_title = "فایل"
    elif class_name == "ourwork":
        class_title = "پروژه"
    elif class_name == "feature":
        class_title = "خدمات"
    elif class_name == "blog":
        class_title = "مقاله"
    elif class_name == "material":
        class_title = "متریال"
    elif class_name == "product":
        class_title = "کالا"
    elif class_name == "vehicle":
        class_title = "وسیله نقلیه"
    elif class_name == "project":
        class_title = "پروژه"
    elif class_name == "service":
        class_title = "سرویس"
    elif class_name=="pm_service":
        class_title = "سرویس"
    elif class_name == "organizationunit":
        class_title = "واحد سازمانی"
    elif class_name == "event":
        class_title = "رویداد"
    elif class_name=="invoice":
        class_title= "فاکتور"
    elif class_name=="maintenance":
        class_title= "تعمیر و نگهداری"
    elif class_name=="materialinvoice":
        class_title= "فاکتور متریال"
    elif class_name=="serviceinvoice":
        class_title ="فاکتور خدمات"
    elif class_name=="workshift":
        class_title= "شیفت کاری"
    elif class_name=="role":
        class_title= "نقش"
    return class_title

class ParameterNameEnum(TextChoices):
    VISITOR_COUNTER="تعداد بازدید",_("تعداد بازدید")
    CURRENCY="واحد پول",_("واحد پول")
    TITLE="عنوان",_("عنوان")
    FARSI_FONT_NAME="نام فونت فارسی",_("نام فونت فارسی")
    HOME_URL="لینک به خانه",_("لینک به خانه")
    THUMBNAIL_DIMENSION="عرض تصاویر کوچک",_("عرض تصاویر کوچک")
    ONLY_HTTPS="فقط https",_("فقط https")
    SHOW_ARCHIVES="نمایش فایل های آرشیو شده",_("نمایش فایل های آرشیو شده")

class TextDirectionEnum(TextChoices):
    Rtl='rtl',_('rtl')
    Ltr='ltr',_('ltr')

def BS_ColorCode(bs_color):
    if bs_color=='success':
        return "#28a745"
    if bs_color=='danger':
        return "#dc3545"
    if bs_color=='warning':
        return "#ffc107"
    if bs_color=='muted':
        return "#34345455"
    if bs_color=='info':
        return "#17a2b8"
    if bs_color=='rose':
        return "#34345455"
    if bs_color=='secondary':
        return "#6c757d"
    if bs_color=='light':
        return "#f8f9fa"
    if bs_color=='dark':
        return "#343a40"
    if bs_color=='primary':
        return "#007bff"
    if bs_color=='blue':
        return "#007bff"
    if bs_color=='indigo':
        return "#6610f2"
    if bs_color=='purple':
        return "#6f42c1"
    if bs_color=='pink':
        return "#e83e8c"
    if bs_color=='red':
        return "#dc3545"
    if bs_color=='orange':
        return "#fd7e14"
    if bs_color=='yellow':
        return "#ffc107"
    if bs_color=='green':
        return "#28a745"
    if bs_color=='teal':
        return "#20c997"
    if bs_color=='cyan':
        return "#17a2b8"
    if bs_color=='white':
        return "#fff"
    if bs_color=='gray':
        return "#6c757d"
    if bs_color=='gray-dark':
        return "#343a40"
   
  

class UnitNameEnum(TextChoices):
    ADAD="عدد",_("عدد")
    GERAM="گرم",_("گرم")
    KILOGERAM="کیلوگرم",_("کیلوگرم")
    TON="تن",_("تن")
    METER="متر",_("متر")
    METER2="متر مربع",_("متر مربع")
    METER3="متر مکعب",_("متر مکعب")
    PART="قطعه",_("قطعه")
    Roll="رول",_("رول")
    SHAKHEH="شاخه",_("شاخه")
    DASTGAH="دستگاه",_("دستگاه")
    SERVICE="سرویس",_("سرویس")
    PACK="بسته",_("بسته")
    POCKET="کیسه",_("کیسه")
    SHOT="شات",_("شات")
    SET="ست",_("ست")
    CUP="فنجان",_("فنجان")
    JOFT="جفت",_("جفت")
    DAST="دست",_("دست")


class IconsEnum(TextChoices):
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    # aaaaaaa='aaaaaaaaaa',_('aaaaaaaaaaa')
    account_circle='account_circle',_('account_circle')
    add_shopping_cart='add_shopping_cart',_('add_shopping_cart')
    apartment='apartment',_('apartment')
    alarm='alarm',_('alarm')
    attach_file='attach_file',_('attach_file')
    attach_money='attach_money',_('attach_money')
    backup='backup',_('backup')
    build='build',_('build')
    card_travel='card_travel',_('card_travel')
    chat='chat',_('chat')
    construction='construction',_('construction')
    dashboard='dashboard',_('dashboard')
    delete='delete',_('delete')
    description='description',_('description')
    emoji_objects='emoji_objects',_('emoji_objects')
    engineering='engineering',_('engineering')
    extension='extension',_('extension')
    face='face',_('face')
    facebook='facebook',_('facebook')
    favorite='favorite',_('favorite')
    fingerprint='fingerprint',_('fingerprint')
    get_app='get_app',_('get_app')
    help_outline='help_outline',_('help_outline')
    home='home',_('home')
    important_devices='important_devices',_('important_devices')
    link='link',_('link')
    linked_camera='linked_camera',_('linked_camera')
    local_shipping='local_shipping',_('local_shipping')
    lock='lock',_('lock')
    mail='mail',_('mail')
    menu='menu',_('menu')
    movie_filter='movie_filter',_('movie_filter')
    network_check='network_check',_('network_check')
    notification_important='notification_important',_('notification_important')
    palette='palette',_('palette')
    phone='phone',_('phone')
    place='place',_('place')
    psychology='psychology',_('psychology')
    publish='publish',_('publish')
    reply='reply',_('reply')
    schedule='schedule',_('schedule')
    school='school',_('school')
    send='send',_('send')
    settings='settings',_('settings')
    share='share',_('share')
    sync='sync',_('sync')
    traffic='traffic',_('traffic')
    two_wheeler='two_wheeler',_('two_wheeler')
    verified_user='verified_user',_('verified_user')
    vpn_key='vpn_key',_('vpn_key')
    weekend='weekend',_('weekend')

class LanguageEnum(TextChoices):
    FARSI="فارسی",_("فارسی")
    ENGLISH="انگلیسی",_("انگلیسی")
    
def LanguageCode(language):
    if language==LanguageEnum.FARSI:
        return 'fa'
    if language==LanguageEnum.ENGLISH:
        return 'en'
def LanguageFromCode(code):
    if code=='fa':
        return LanguageEnum.FARSI
    if code=='en':
        return LanguageEnum.ENGLISH
   
class PictureNameEnum(TextChoices):
    LOGO="لوگو",_("لوگو")
    FAVICON="آیکون",_("آیکون")
    BACKGROUND="پس زمینه",_("پس زمینه")
    
class ColorEnum(TextChoices):
    SUCCESS = 'success', _('success')
    DANGER = 'danger', _('danger')
    WARNING = 'warning', _('warning')
    PRIMARY = 'primary', _('primary')
    MUTED = 'muted', _('muted')
    SECONDARY = 'secondary', _('secondary')
    INFO = 'info', _('info')
    LIGHT = 'light', _('light')
    ROSE = 'rose', _('rose')
    DARK = 'dark', _('dark') 
