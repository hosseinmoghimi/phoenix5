from django.urls import path
from health.apps import APP_NAME
from health import views,apis



from django.contrib.auth.decorators import login_required


app_name=APP_NAME
urlpatterns = [
    
    path("",login_required(views.HomeViews.as_view()),name="home"),
    path("search/",login_required(views.SearchView.as_view()),name="search"),
    path("patients/",login_required(views.PatientsView.as_view()),name="patients"),
    path("patient/<int:pk>/",login_required(views.PatientView.as_view()),name="patient"),
    
    path("drugs/",login_required(views.DrugsView.as_view()),name="drugs"),
    path("drug/<int:pk>/",login_required(views.DrugView.as_view()),name="drug"),

    
    path("add_drug/",login_required(apis.AddDrugApi.as_view()),name="add_drug"),
    path("add_patient/",login_required(apis.AddPatientApi.as_view()),name="add_patient"),
]
