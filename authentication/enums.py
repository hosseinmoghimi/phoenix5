from django.utils.translation import gettext as _
from django.db.models import TextChoices

class ProfileStatusEnum(TextChoices):
    AAA="AAA" , _("AAA")
    BBB="BBB" , _("BBB")

class AUTH_PictureNameEnum(TextChoices):
    LOGIN_FORM_HEADER="سربرگ فرم لاگین" , _("سربرگ فرم لاگین")
    REGISTER_FORM_HEADER="سربرگ فرم ثبت نام" , _("سربرگ فرم ثبت نام")
    CHANGE_PASSWORD_FORM_HEADER="سربرگ فرم تغییر کلمه عبور" , _("سربرگ فرم تغییر کلمه عبور")
