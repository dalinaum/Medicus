"""Medicus 모듈의 뷰"""
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
    """
    의사 검색을 의한 뷰입니다. search_fields를 지정해서
    의사 정보에서 검색할 키워드를 처리할 수 있게 하였습니다.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSereailizer
    filter_backends = [filters.SearchFilter]
    search_fields = ['specialties__name', "name",
                     "office_name", "non_reimbursable"]


class AvailableDoctorList(generics.ListAPIView):
    """
    시간에 맞추어 진료가능한 의사를 찾는 뷰입니다.
    """
    serializer_class = DoctorSereailizer

    def get_queryset(self):
        """
        해당 시간에 맞는 의사 queryset을 반환합니다.
        return: 요일과 시간에 맞는 의사 queryset
        """
        candidate = self.kwargs['candidate']
        weekday = candidate.weekday() + 1
        time = candidate.time()
        queryset = get_available_doctors(weekday, time)
        return queryset


class CreateAppointment(generics.CreateAPIView):
    """
    진료 요청을 처리하는 뷰입니다.

    진료 요청이 올바른지는 CreateAppointmentSerializer에서
    판단하게 하였습니다. View와 Seriailizer 중에 어디에서
    처리하는 것이 좋을까 고민해보았고 이번에는 Serializer에서
    처리를 해보았습니다.
    """
    serializer_class = CreateAppointmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListAppointment(generics.ListAPIView):
    """
    진료 요청을 보여주는 뷰입니다.
    아직 승락하지않은 진료 요청에 대해서만 보여줍니다.
    """
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        specific_doctor = Q(doctor_id=doctor_id)
        not_accepted = Q(accepted=False)
        return Appointment.objects.filter(specific_doctor & not_accepted)


class AcceptAppointment(APIView):
    """
    진료 요청을 승락하는 뷰입니다.

    아직 expiration이 지나지 않았어야만 승락합니다.
    """

    def patch(self, _, appointment_id):
        """
        PATCH 메서드에 맞추어 요청을 처리합니다. 진료요청을 받을 수 있는
        시간인지 확인 후에 승락 여부를 처리합니다.

        :param request: request는 사용하지 않습니다.
        :param appointment_id: 승락할 진료 id입니다.
        :return 진료 승락한 요청을 리스폰스에 담아 반환합니다.
        """
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
