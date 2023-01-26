from core.enums import _,TextChoices

class ParameterMarketEnum(TextChoices):
    SHOP_HEADER_TITLE="SHOP_HEADER_TITLE",_("SHOP_HEADER_TITLE")
    SHOP_HEADER_SLOGAN="SHOP_HEADER_SLOGAN",_("SHOP_HEADER_SLOGAN")
    SHOP_HEADER_IMAGE="SHOP_HEADER_IMAGE",_("SHOP_HEADER_IMAGE")

class CustomerLevelEnum(TextChoices):
    REGULAR="مشتری عادی",_("مشتری عادی")
    CO_WROKER="همکار",_("همکار")
