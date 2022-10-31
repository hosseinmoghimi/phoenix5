from guarantee.apps import APP_NAME
from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
app_name=APP_NAME
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('guarantee/<int:pk>/',login_required(views.GuaranteeViews.as_view()),name="guarantee"),
    path('guarantees/',login_required(views.GuaranteesViews.as_view()),name="guarantees"),
    path('add_guarantee/',login_required(apis.AddGuaranteeApi.as_view()),name="add_guarantee"),

]
