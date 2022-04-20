from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from bms.apps import APP_NAME
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name='home'),
    path('feeders/',login_required(views.FeedersView.as_view()),name='feeders'),
    path('feeder/<int:pk>/',login_required(views.FeederView.as_view()),name='feeder'),
    path('relay/<int:pk>/',login_required(views.FeedersView.as_view()),name='relay'),
    path('command/<int:pk>/',login_required(views.FeedersView.as_view()),name='command'),
    path('scenario/<int:pk>/',login_required(views.FeedersView.as_view()),name='scenario'),
    
]
