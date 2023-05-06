# from django.shortcuts import render
from rest_framework import viewsets, filters, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializiers import DoctorSereailizer
from .models import Doctor

from rest_framework import filters


class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSereailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialties__name', "name",
                     "office_name", "non_reimbursable"]
