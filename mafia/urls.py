from mafia.apps import APP_NAME
from django.urls import path
from mafia import views,apis

app_name=APP_NAME
urlpatterns = [
    path("",views.HomeView.as_view(),name="home"),
    
    path("roles/",views.RolesView.as_view(),name="roles"),
    path("role/<int:pk>/",views.RoleView.as_view(),name="role"),
    path("add_role/",apis.AddRoleApi.as_view(),name="add_role"),
    path("add_role_to_game/",apis.AddRoleToGameApi.as_view(),name="add_role_to_game"),
    
    path("role_players/",views.RolePlayersView.as_view(),name="role_players"),
    path("role_player/<int:pk>/",views.RolePlayerView.as_view(),name="roleplayer"),
    path("add_role/",apis.AddRoleApi.as_view(),name="add_role_player"),

    
    path("players/",views.PlayersView.as_view(),name="players"),
    path("player/<int:pk>/",views.PlayerView.as_view(),name="player"),
    path("add_player/",apis.AddPlayerApi.as_view(),name="add_player"),
    
    path("leages/",views.GamesView.as_view(),name="leages"),
    path("leage/<int:pk>/",views.GameView.as_view(),name="leage"),
    
    path("games/",views.GamesView.as_view(),name="games"),
    path("game/<int:pk>/",views.GameView.as_view(),name="game"),
    path("add_game/",views.AddGameView.as_view(),name="add_game"),


    path("gods/",views.GodsView.as_view(),name="gods"),
    path("god/<int:pk>/",views.GodView.as_view(),name="god"),
    path("add_god/",apis.AddGodApi.as_view(),name="add_god"),

    path("game_act/<int:pk>/",views.GameActView.as_view(),name="gameact"),
    path("add_player_to_game/",apis.AddPlayerToGameApi.as_view(),name="add_player_to_game"),
    path("add_game_act/",views.GameActView.as_view(),name="add_game_act"),

    path("game_scenarioes/",views.GameScenarioesView.as_view(),name="game_scenarioes"),
    path("game_scenario/<int:pk>/",views.GameScenarioView.as_view(),name="gamescenario"),
    path("add_game_scenarios/",apis.AddRoleApi.as_view(),name="add_game_scenarios"),


    path("initialize/",views.InitializeView.as_view(),name="initialize"),


]
