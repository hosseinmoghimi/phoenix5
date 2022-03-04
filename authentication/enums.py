from django.utils.translation import gettext as _
from django.db.models import TextChoices

class ProfileStatusEnum(TextChoices):
    AAA="AAA" , _("AAA")
    BBB="BBB" , _("BBB")
