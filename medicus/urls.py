from django.urls import path, register_converter
from .converters import DateTimeConverter
from . import views


register_converter(DateTimeConverter, 'datetime')

urlpatterns = [
    path("doctor/", views.DoctorList.as_view()),
    path("doctor/<datetime:candidate>/", views.AvailableDoctorList.as_view()),
    path("doctor/<int:doctor_id>/appointment/", views.CreateAppointment.as_view()),
]
