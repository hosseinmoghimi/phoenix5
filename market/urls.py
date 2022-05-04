from .apps import APP_NAME
from . import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("search/",(views.SearchView.as_view()),name="search"),

    path("product/<int:pk>/",login_required(views.HomeView.as_view()),name="product"),

    path("brands/",login_required(views.HomeView.as_view()),name="brands"),

    path("category/<int:pk>/",login_required(views.CategoryView.as_view()),name="category"),

    path("ware_houses/",login_required(views.HomeView.as_view()),name="ware_houses"),
    
    path("suppliers/",login_required(views.HomeView.as_view()),name="suppliers"),
    path("supplier/<int:pk>/",login_required(views.HomeView.as_view()),name="supplier"),


    path("api/categories/",(apis.CategoriesApi.as_view()),name="api_categories"),
    path("api/category/<int:category_id>/",(apis.CategoryApi.as_view()),name="api_category"),
    path("api/products/<int:category_id>/",(apis.ProductsApi.as_view()),name="api_category_products"),
    
]
