# from django.shortcuts import render
from rest_framework import filters, generics
from .serializiers import DoctorSereailizer
from .models import Doctor


class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSereailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialties__name', "name",
                     "office_name", "non_reimbursable"]
