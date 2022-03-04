from django.apps import AppConfig

from core.apps import APP_NAME

APP_NAME="accounting"
class AccountingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting'
