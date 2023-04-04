from django.urls import path
from . import views,apis
from core.urls import login_required
from .apps import APP_NAME


app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.IndexView.as_view()),name="home"),
    path("category/<int:pk>",login_required(views.CategoryView.as_view()),name="category"),
    path("product/<int:pk>",login_required(views.ProductView.as_view()),name="product"),
]
