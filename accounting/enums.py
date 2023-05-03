from django.utils.translation import gettext as _
from django.db.models import TextChoices
from core.enums import ColorEnum, UnitNameEnum


class FinancialDocumentDirectionEnum(TextChoices):
    BEDEHKAR="بدهکار",_("بدهکار")
    BESTANKAR="بستانکار",_("بستانکار")


class WareHouseSheetDirectionEnum(TextChoices):
    IMPORT="ورود به انبار",_("ورود به انبار")
    EXPORT="خروج از انبار",_("خروج از انبار")
 

class ParameterAccountingEnum(TextChoices):
    COUNT_OF_ITEM_PER_PAGE="تعداد آیتم در صفحه",_("تعداد آیتم در صفحه")

class ChequeStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    RETURNED="برگشت خورده",_("برگشت خورده")
    PASSED="پاس شده",_("پاس شده")
    PAID="تسویه شده",_("تسویه شده")

def getColor(title):
    color=ColorEnum.PRIMARY
    if title==FinancialBalanceTitleEnum.ASSET:
        color=ColorEnum.SUCCESS
    if title==FinancialBalanceTitleEnum.MISC:
        color=ColorEnum.MUTED
    if title==FinancialBalanceTitleEnum.PROPERTY:
        color=ColorEnum.SUCCESS
    if title==FinancialBalanceTitleEnum.ASSET:
        color=ColorEnum.SUCCESS
    if title==FinancialBalanceTitleEnum.FURNITURE:
        color=ColorEnum.WARNING
    if title==FinancialBalanceTitleEnum.SELL:
        color=ColorEnum.INFO
    if title==FinancialBalanceTitleEnum.BUY:
        color=ColorEnum.DANGER
    return color

class SpendTypeEnum(TextChoices):
    COST="هزینه",("هزینه")
    WAGE="حقوق",("حقوق")


class CostTypeEnum(TextChoices):
    WATER="هزینه آب",_("هزینه آب")
    RENT="هزینه اجاره",_("هزینه اجاره")
    INTERNET="هزینه اینترنت",_("هزینه اینترنت")
    ELECTRICITY="هزینه برق",_("هزینه برق")
    TELEPHONE="هزینه تلفن",_("هزینه تلفن")
    TRANSPORT="هزینه حمل ونقل",_("هزینه حمل ونقل")
    FOOD="هزینه خوراک",_("هزینه خوراک")
    MEDICAL="هزینه دارو و سلامت",_("هزینه دارو و سلامت")
    GAS="هزینه گاز",_("هزینه گاز")
    MOBILE="هزینه موبایل",_("هزینه موبایل")


class PaymentMethodEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    # NO_PAYMENT="پرداخت نشده",_("پرداخت نشده")
    MOBILE_BANK="همراه بانک",_("همراه بانک")
    PRODUCT="فروش کالا",_("فروش کالا")
    SERVICE="فروش خدمات",_("فروش خدمات")
    IN_CASH="نقدی",_("نقدی")
    CHEQUE="چک",_("چک")
    POS="کارتخوان",_("کارتخوان")
    BANK_FISH="فیش بانکی",_("فیش بانکی")
    CARD="کارت به کارت",_("کارت به کارت")
    # FROM_PAST="مانده حساب از قبل",_("مانده حساب از قبل")

class TransactionStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    IN_PROGRESS="در جریان",_("در جریان")
    READY="آماده تحویل",_("آماده تحویل")
    APPROVED="تایید شده",_("تایید شده")
    DELIVERED="تحویل شده",_("تحویل شده")
    CANCELED="کنسل شده",_("کنسل شده")
    ROLL_BACKED="برگشت از تحویل",_("برگشت از تحویل")
    FINISHED="تایید نهایی شده",_("تایید نهایی شده")
    PASSED="پاس شده",_("پاس شده")
    FROM_PAST="مانده حساب از قبل",_("مانده حساب از قبل")

class FinancialDocumentStatusEnum(TextChoices):
    DRAFT="پیش نویس",_("پیش نویس")
    IN_PROGRESS="در جریان",_("در جریان")
    DELIVERED="تحویل شده",_("تحویل شده")
    APPROVED="تایید شده",_("تایید شده")
    CANCELED="کنسل شده",_("کنسل شده")
    ROLL_BACKED="برگشت از تحویل",_("برگشت از تحویل")
    FINISHED="تایید نهایی شده",_("تایید نهایی شده")
    PASSED="پاس شده",_("پاس شده")
    FROM_PAST="مانده حساب از قبل",_("مانده حساب از قبل")

class FinancialBalanceTitleEnum(TextChoices):
    REGULAR="حساب عادی",_("حساب عادی")
    INVESTMENT="سرمایه گذاری",_("سرمایه گذاری")
    ASSET="دارایی",_("دارایی")
    PROPERTY="ملک",_("ملک")
    FURNITURE="اثاثیه",_("اثاثیه")
    TAX="مالیات",_("مالیات")
    COST="هزینه",_("هزینه")
    WAGE="حقوق",_("حقوق")
    SELL="فروش",_("فروش")
    BUY="خرید",_("خرید")
    MISC="سایر",_("سایر")
