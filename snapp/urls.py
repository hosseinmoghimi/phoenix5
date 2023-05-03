from django.urls import path
from . import views,apis
from core.urls import login_required
from .apps import APP_NAME


app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.IndexView.as_view()),name="home"),
    path("category/<int:pk>",login_required(views.CategoryView.as_view()),name="category"),
    path("product/<int:pk>",login_required(views.ProductView.as_view()),name="product"),
    path("menu/<int:pk>",login_required(views.MenuView.as_view()),name="menu"),
    path("categories/",login_required(views.CategoriesView.as_view()),name="categories"),
    path("menus/",login_required(views.MenusView.as_view()),name="menus"),
    path("add_menu/",login_required(apis.AddMenuView.as_view()),name="add_menu"),
]
