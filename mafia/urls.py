from mafia.apps import APP_NAME
from django.urls import path
from mafia import views,apis

app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    
    path("roles/",views.RolesView.as_view(),name="roles"),
    path("role/<int:pk>/",views.RoleView.as_view(),name="role"),
    path("add_role/",apis.AddRoleApi.as_view(),name="add_role"),
    
    path("role_players/",views.RolePlayersView.as_view(),name="role_players"),
    path("role_player/<int:pk>/",views.RolePlayerView.as_view(),name="roleplayer"),
    path("add_role/",apis.AddRoleApi.as_view(),name="add_role_player"),
    
    path("players/",views.RolesView.as_view(),name="players"),
    path("player/<int:pk>/",views.RoleView.as_view(),name="player"),
    path("add_player/",apis.AddRoleApi.as_view(),name="add_player"),


]
