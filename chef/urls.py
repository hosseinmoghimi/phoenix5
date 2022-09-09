from chef.apps import APP_NAME
from chef import views,apis
from django.contrib.auth.decorators import login_required
from django.urls import path
app_name=APP_NAME
urlpatterns = [
    path("",(views.HomeView.as_view()),name="home"),
    path("search/",(views.SearchView.as_view()),name="search"),
    path("food/",login_required(views.FoodsView.as_view()),name="foods"),
    path("food/<int:pk>/",(views.FoodView.as_view()),name="food"),
    path("add_food/",login_required(apis.AddFoodApi.as_view()),name="add_food"),
]
