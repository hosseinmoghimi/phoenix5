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

    path("guests/",login_required(views.GuestsView.as_view()),name="guests"),
    path("guest/<int:pk>/",login_required(views.GuestView.as_view()),name="guest"),

    path("hosts/",login_required(views.HostsView.as_view()),name="hosts"),
    path("host/<int:pk>/",login_required(views.HostView.as_view()),name="host"),


    path("meals/<int:guest_id>/",login_required(views.MealsView.as_view()),name="meals"),
    path("meal/<int:pk>/",login_required(views.MealView.as_view()),name="meal"),
    
    path('reserve_meal/',apis.ReserveMealApi.as_view(),name="reserve_meal"),
    path('add_meal/',apis.AddFoodApi.as_view(),name="add_meal"),
    path('unreserve_meal/',apis.AddFoodApi.as_view(),name="unreserve_meal"),
    path('serve_meal/',apis.AddFoodApi.as_view(),name="serve_meal"),
    path('unserve_meal/',apis.AddFoodApi.as_view(),name="unserve_meal"),

]
