from django.db.models import TextChoices
from django.utils.translation import gettext as _


class ParameterNameEnum(TextChoices):
    OFFICE_ADDRESS="آدرس دفتر",_("آدرس دفتر")
    OFFICE_TEL="تلفن دفتر",_("تلفن دفتر")
    OFFICE_EMAIL="ایمیل دفتر",_("ایمیل دفتر")
    OFFICE_MOBILE="شماره همراه",_("شماره همراه")

    
class ParameterEnum(TextChoices):
    CONTACT_US_TITLE="عنوان ارتباط با ما",_("عنوان ارتباط با ما")
    CONTACT_US_DESCRIPTION="توضیح ارتباط با ما",_("توضیح ارتباط با ما")
    OFFICE_ADDRESS="آدرس دفتر",_("آدرس دفتر")
    OFFICE_TEL="تلفن دفتر",_("تلفن دفتر")
    OFFICE_MOBILE="تماس  دفتر",_("تماس  دفتر")
    OFFICE_EMAIL="ایمیل دفتر",_("ایمیل دفتر")
    FEATURES_TITLE="عنوان خدمات ما",_("عنوان خدمات ما")
    FEATURES_DESCRIPTION="توضیح خدمات ما",_("توضیح خدمات ما")
    BLOGS_TITLE="عنوان مقالات",_("عنوان مقالات")
    BLOGS_DESCRIPTION="توضیح مقالات",_("توضیح مقالات")
    OUR_WORKS_PRE_TITLE="پیش عنوان پروژه های ما",_("پیش عنوان پروژه های ما")
    OUR_WORKS_TITLE="عنوان پروژه های ما",_("عنوان پروژه های ما")
    OUR_WORKS_DESCRIPTION="توضیح پروژه های ما",_("توضیح پروژه های ما")
    OURWORKS_TITLE="عنوان تیم ما",_("عنوان تیم ما")
    OUR_TEAMS_DESCRIPTION="توضیح تیم ما",_("توضیح تیم ما")
    TESTIMONIAL_TITLE="عنوان گفته هایی مورد ما",_("عنوان گفته هایی مورد ما")

