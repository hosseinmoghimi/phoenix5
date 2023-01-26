from .models import _
from django.db.models import TextChoices

class MealTypeEnum(TextChoices):
    BREAK_FAST="صبحانه",_("صبحانه")
    LUNCH="ناهار",_("ناهار")
    DINNER="شام",_("شام")