from django.shortcuts import render
from .apps import APP_NAME
from . import views,apis
from django.urls import path,include


from django.contrib.auth.decorators import login_required

app_name=APP_NAME
urlpatterns = [
    path('',login_required(views.BasicViews().home),name="home"),
    
    path('books/',login_required(views.BooksView.as_view()),name="books"),
    path('book/<int:pk>/',(views.BookView.as_view()),name="book"),
    path('book/<int:pk>',(views.BookView.as_view()),name="book_"),
    
    path('members/',login_required(views.MembersView.as_view()),name="members"),
    path('member/<int:pk>/',login_required(views.MemberView.as_view()),name="member"),
    
    path('lends/',login_required(views.LendViews().lends),name="lends"),
    path('lend/<int:pk>/',login_required(views.LendViews().lend),name="lend"),

    path('lend/<int:pk>/',login_required(views.BookView.as_view()),name="lend"),
    path('add_book/',login_required(apis.AddBookApi.as_view()),name="add_book"),
    path('add_member/',login_required(apis.AddMemberApi.as_view()),name="add_member"),
    path('add_lend/',login_required(apis.LendBookApi.as_view()),name="add_lend"),
]


