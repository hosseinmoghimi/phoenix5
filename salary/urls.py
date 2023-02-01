from django.urls import path
from . import views,apis
from django.contrib.auth.decorators import login_required
from .apps import APP_NAME


app_name=APP_NAME
urlpatterns = [
    path("",login_required(views.IndexView.as_view()),name="home"),
    path("groups/",login_required(views.GroupsView.as_view()),name="groups"),
    path("group/<int:pk>/",login_required(views.GroupView.as_view()),name="group"),
    path("salary/<int:pk>/",login_required(views.SalaryView.as_view()),name="salary"),
    path("employee/<int:pk>/",login_required(views.EmployeeView.as_view()),name="employee"),
    path("employee/<int:pk>/<int:year>/",login_required(views.EmployeeView.as_view()),name="employee_year"),
    path("employee/<int:pk>/<int:year>/<int:month>/",login_required(views.EmployeeView.as_view()),name="employee_month"),

    path("add_group/",login_required(apis.AddGroupApi.as_view()),name="add_group"),
    path("add_salary/",login_required(apis.AddSalaryApi.as_view()),name="add_salary"),
]
