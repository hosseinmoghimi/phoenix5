from django.urls import path
from polls.apps import APP_NAME
from django.contrib.auth.decorators import login_required
from polls import views,apis
app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.HomeView.as_view()),name="home"),
    path('polls/',login_required(views.PollsView.as_view()),name="polls"),
    path('poll/<int:pk>/',login_required(views.PollView.as_view()),name="poll"),
    path('add_poll/',login_required(apis.AddPollApi.as_view()),name="add_poll"),
    path('add_option/',login_required(apis.AddOptionApi.as_view()),name="add_option"),
    path('option/<int:pk>/',login_required(views.OptionView.as_view()),name="option"),
]
