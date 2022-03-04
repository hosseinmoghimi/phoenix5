from django.core.files.storage import FileSystemStorage
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL, UPLOAD_ROOT
from tinymce.models import HTMLField
from utility.calendar import PersianCalendar
from utility.utils import LinkHelper

from .apps import APP_NAME
from .enums import *

IMAGE_FOLDER="images"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')
