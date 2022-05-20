from core.enums import TextChoices,_


class OrganizationParameterEnum(TextChoices):
    SHOW_ARCHIVE_PAGES="نمایش صفحات آرشیو شده",_("نمایش صفحات آرشیو شده")

class LetterStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    LOCKED="قفل شده",_("قفل شده")
    ARCHIVED="آرشیو شده",_("آرشیو شده")