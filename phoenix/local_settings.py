

from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = ['*']

SITE_FULL_BASE_ADDRESS="https://cryptalx.com/"
UPLOAD_ROOT="d:\\phoenix5\\uploads"
ALLOW_REGISTER_ONLINE=False
DEBUG=True
SITE_URL='/'


HOME_APP_URLS='projectmanager.urls'
PUBLIC_ROOT=os.path.join(BASE_DIR,'public_html')
QRCODE_ROOT=os.path.join(PUBLIC_ROOT,'qrcode')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    'django_social_share',
    
    'rest_framework',
    # 'rest_framework.authtoken'
    # 'web3auth.apps.Web3AuthConfig',
    'realestate',
    'market',
    'health',
    'scheduler',
    'resume',
    'core',
    'wallet',
    'authentication',
    'utility',
    'dashboard',
    'tinymce',
    'accounting',
    'projectmanager',
    'web',
    'stock',
    'polls',
    'transport',
    'guarantee',
    'chef',
    'log',
    'map',
    'archive',
    'messenger',
    'warehouse',
    'organization',
    'library',
    'mafia',
    'school',
    'bms',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db20220706.sqlite3',
    }
}
SECRET_KEY = 'django-insecure-bt+o^tb1w_vl6vj%tjn-&=v5^m*w3)5a8(i&uoo)6on&pi-x6('

TIME_ZONE = 'Asia/Tehran'


STATIC_ROOT=os.path.join(PUBLIC_ROOT,'static')
MEDIA_ROOT=os.path.join(PUBLIC_ROOT,'media')
STATIC_URL = SITE_URL+'static/'
MEDIA_URL =  SITE_URL+'media/'
ADMIN_URL=SITE_URL+"admin/"
QRCODE_URL=SITE_URL+"qrcode/"

STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]




phoenix_apps=[
    {
        'name':'authentication',
        'title':'هویت',
        'color':'warning',
        'home_url':SITE_URL+"authentication"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'health',
        'title':'بهداشت',
        'color':'success',
        'home_url':SITE_URL+"health"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'polls',
        'title':'نظرسنجی',
        'color':'success',
        'home_url':SITE_URL+"polls"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'mafia',
        'title':'مافیا',
        'color':'warning',
        'home_url':SITE_URL+"mafia"+"/",
        'has_help':False,
        'show_on_menu':True,
    },

    {
        'name':'organization',
        'title':'سازمان',
        'color':'danger',
        'home_url':SITE_URL+"organization"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'library',
        'title':'کتابخانه',
        'color':'success',
        'home_url':SITE_URL+"library"+"/",
        'has_help':False,
        'show_on_menu':True,
    },

    
    {
        'name':'bms',
        'title':'هوشمند سازی',
        'color':'info',
        'home_url':SITE_URL+"bms"+"/",
        'has_help':False,
        'show_on_menu':True,
    },


    {
        'name':'scheduler',
        'title':'برنامه ریز',
        'color':'primary',
        'home_url':SITE_URL+"scheduler"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'school',
        'title':'آموزشگاه',
        'color':'warning',
        'home_url':SITE_URL+"school"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'chef',
        'title':'سرآشپز',
        'color':'danger',
        'home_url':SITE_URL+'chef/',
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'resume',
        'title':'رزومه',
        'color':'success',
        'home_url':SITE_URL+"resume"+"/",
        'has_help':False,
        'show_on_menu':False,
    },
    {
        'name':'guarantee',
        'title':'گارانتی',
        'color':'warning',
        'home_url':SITE_URL+"guarantee"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'warehouse',
        'title':'انبار',
        'color':'warning',
        'home_url':SITE_URL+"warehouse"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'wallet',
        'title':'کیف پول',
        'color':'warning',
        'home_url':SITE_URL+"wallet"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'log',
        'title':'لاگ',
        'color':'warning',
        'home_url':SITE_URL+"log"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'messenger',
        'title':'پیام رسان',
        'color':'warning',
        'home_url':SITE_URL+"messenger"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'archive',
        'title':'آرشیو',
        'color':'warning',
        'home_url':SITE_URL+"archive"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'utility',
        'color':'danger',
        'title':'ابزار های کاربردی',
        'home_url':SITE_URL+"utility"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'projectmanager',
        'color':'success',
        'title':'مدیریت پروژه',
        'home_url':SITE_URL+"pm"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'realestate',
        'color':'success',
        'title':'املاک',
        'home_url':SITE_URL+"realestate"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'core',
        'title':'core',
        'color':'danger',
        'home_url':SITE_URL+"core"+"/",
        'has_help':False,
        'show_on_menu':False,
    },

    
    {
        'name':'transport',
        'title':'حمل و نقل',
        'color':'danger',
        'home_url':SITE_URL+"transport"+"/",
        'has_help':False,
        'show_on_menu':True,
    },

    
    {
        'name':'map',
        'title':'نقشه',
        'color':'danger',
        'home_url':SITE_URL+"map"+"/",
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'market',
        'title':'مارکت',
        'color':'danger',
        'home_url':SITE_URL+'market/',
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'accounting',
        'title':'حسابداری',
        'color':'danger',
        'home_url':SITE_URL+'accounting/',
        'has_help':False,
        'show_on_menu':True,
    },
    {
        'name':'stock',
        'title':'سهام',
        'color':'danger',
        'home_url':SITE_URL+'stock/',
        'has_help':False,
        'show_on_menu':True,
    },

    {
        'name':'web',
        'title':'وب سایت',
        'color':'success',
        'home_url':SITE_URL+'web/',
        'has_help':False,
        'show_on_menu':True,
    },
]    