from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("patients/", views.patient_list, name="patient_list"),
    path("patients/add/", views.patient_create, name="patient_add"),
    path("patients/<int:pk>/", views.patient_detail, name="patient_detail"),
    path("patients/<int:pk>/edit/", views.patient_update, name="patient_edit"),
    path("patients/<int:patient_pk>/consultations/add/", views.encounter_create, name="encounter_add"),
    path("consultations/<int:encounter_pk>/prescriptions/add/", views.prescription_add, name="prescription_add"),
]
