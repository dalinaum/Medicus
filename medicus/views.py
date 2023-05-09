import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import filters, generics, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializiers import DoctorSereailizer, CreateAppointmentSerializer, AppointmentSerializer
from .models import Appointment, Doctor
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


class ListAppointment(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        specific_doctor = Q(doctor_id=doctor_id)
        not_accepted = Q(accepted=False)
        return Appointment.objects.filter(specific_doctor & not_accepted)


class AcceptAppointment(APIView):
    def patch(self, request, appointment_id):
        instance = get_object_or_404(Appointment, id=appointment_id)
        if instance.expiration < datetime.datetime.now().astimezone():
            raise serializers.ValidationError(
                "진료 요청을 수락할 수 있는 시간이 지났습니다."
            )
        serializer = AppointmentSerializer(instance, data={}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['accepted'] = True
        serializer.validated_data['accepted_at'] = datetime.datetime.now()
        serializer.save()
        return Response(serializer.data)
