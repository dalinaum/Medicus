from django.urls import path, include
from . import views

urlpatterns = [
    path("doctor/", views.DoctorList.as_view()),
]