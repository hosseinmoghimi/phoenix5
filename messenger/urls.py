from django.urls import path
from messenger import views,apis
from messenger.apps import APP_NAME
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.HomeViews.as_view()),name="home"),
    path("message/<int:pk>/",login_required(views.MessageViews.as_view()),name="message"),
    path("channel/<int:pk>/",login_required(views.ChannelViews.as_view()),name="channel"),
    # path("event/<int:pk>/",views.EventViews().event,name="event"),
    path("member/<int:pk>/",login_required(views.MemberView.as_view()),name="member"),

    
    path("send_message/",login_required(apis.SendMessageApi.as_view()),name="send_message"),
    path("send_notification/",login_required(apis.SendNotificationApi.as_view()),name="send_notification"),
]
