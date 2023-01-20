from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
from .apps import APP_NAME


app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.IndexView.as_view()),name="home"),
    path("contacts/",login_required(views.ContactsView.as_view()),name="contacts"),





    
    path("add_contact/",login_required(apis.AddContactApi.as_view()),name="add_contact"),
]
