from core.enums import _,TextChoices


class RoleSideEnum(TextChoices):
    MAFIA="مافیا",_("مافیا")
    CITIZEN="شهروند",_("شهروند")
    INDEPENDENT="مستقل",_("مستقل")

    
class GameStatusEnum(TextChoices):
    INITIAL="ایجاد شده",_("ایجاد شده")
    PLAYER_ADDING="در حال افزودن بازیکنان",_("در حال افزودن بازیکنان")
    ROLE_ADDING="در حال افزودن نقش",_("در حال افزودن بازیکنان")
    STARTED="شروع شده",_("شروع شده")
    ENDED="پایان یافته",_("پایان یافته")
