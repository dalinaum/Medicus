# from django.shortcuts import render
from django.db.models import Q
from rest_framework import filters, generics
from .serializiers import DoctorSereailizer
from .models import Doctor


class DoctorList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSereailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialties__name', "name",
                     "office_name", "non_reimbursable"]


class AvailableDoctorList(generics.ListAPIView):
    serializer_class = DoctorSereailizer

    def get_queryset(self):
        candidate = self.kwargs['candidate']
        weekday = candidate.weekday() + 1
        time = candidate.time()
        valid_weekday = Q(opening_hours__weekday=weekday)
        valid_opening_hour = Q(
            Q(opening_hours__from_hour__lte=time) &
            Q(opening_hours__to_hour__gte=time)
        )
        not_lunchtime = Q(
            Q(opening_hours__lunch_hour__isnull=True) |
            ~Q(
                Q(opening_hours__lunch_hour__lte=time) &
                Q(opening_hours__lunch_end_hour__gte=time)
            )
        )
        queryset = Doctor.objects.filter(
            valid_weekday & valid_opening_hour & not_lunchtime)
        return queryset
