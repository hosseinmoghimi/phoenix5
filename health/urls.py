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
    
    path("visits/",login_required(views.VisitsView.as_view()),name="visits"),
    path("visit/<int:pk>/",login_required(views.VisitView.as_view()),name="visit"),
    
    path("diseases/",login_required(views.DiseasesView.as_view()),name="diseases"),
    path("disease/<int:pk>/",login_required(views.DiseaseView.as_view()),name="disease"),
    
    path("doctors/",login_required(views.DoctorsView.as_view()),name="doctors"),
    path("doctor/<int:pk>/",login_required(views.DoctorView.as_view()),name="doctor"),
    
    path("drugs/",login_required(views.DrugsView.as_view()),name="drugs"),
    path("drug/<int:pk>/",login_required(views.DrugView.as_view()),name="drug"),

    
    path("add_drug/",login_required(apis.AddDrugApi.as_view()),name="add_drug"),
    path("add_patient/",login_required(apis.AddPatientApi.as_view()),name="add_patient"),
    path("add_disease/",login_required(apis.AddDiseaseApi.as_view()),name="add_disease"),
    path("add_doctor/",login_required(apis.AddDoctorApi.as_view()),name="add_doctor"),
]
