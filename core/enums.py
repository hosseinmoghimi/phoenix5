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



class ParameterNameEnum(TextChoices):
    VISITOR_COUNTER="تعداد بازدید",_("تعداد بازدید")
    CURRENCY="واحد پول",_("واحد پول")
    TITLE="عنوان",_("عنوان")
    FARSI_FONT_NAME="نام فونت فارسی",_("نام فونت فارسی")
    HOME_URL="لینک به خانه",_("لینک به خانه")

    THUMBNAIL_DIMENSION="عرض تصاویر کوچک",_("عرض تصاویر کوچک")

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
