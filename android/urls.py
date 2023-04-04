from .apps import APP_NAME
from . import views
from django.urls import path
app_name=APP_NAME

urlpatterns = [
    path("",views.Categories.as_view(),name="home"),
    path("categories/",views.Categories.as_view(),name="categories"),
    path("products/<int:category_id>/",views.Products.as_view(),name="products"),
]
 