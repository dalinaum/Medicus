from rest_framework import filters, generics, status
from rest_framework.response import Response
from .serializiers import DoctorSereailizer, CreateAppointmentSerializer
from .models import Doctor
from .utils import get_available_doctors


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
        queryset = get_available_doctors(weekday, time)
        return queryset


class CreateAppointment(generics.CreateAPIView):
    serializer_class = CreateAppointmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
