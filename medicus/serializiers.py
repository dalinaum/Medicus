"""Medicus 모듈의 Serializer들"""
import datetime
from rest_framework import serializers
from . import models
from .utils import get_available_doctors


class MedicalSpecialtySerializer(serializers.ModelSerializer):
    """
    진료과목에 대한 Serializer
    """
    class Meta:
        """
        진료과목 모델의 모든 항목을 가져오도록 설정하는 메타정보
        """
        model = models.MedicalSpecialty
        fields = '__all__'


class OpeningHourSerializer(serializers.ModelSerializer):
    """
    영업시간에 관련한 Serialzier
    """
    class Meta:
        """
        영업시간에 관한 설정 일부 필드만 가져와서 지정.
        """
        model = models.OpeningHour
        fields = [
            'weekday',
            'from_hour',
            'to_hour',
            'lunch_hour',
            'lunch_end_hour'
        ]


class DoctorSereailizer(serializers.ModelSerializer):
    """
    의사에대한 시리얼라이저, 진료과목과 영업시간을 포함함.
    """
    specialties = MedicalSpecialtySerializer(many=True)
    opening_hours = OpeningHourSerializer(many=True)

    class Meta:
        """
        Doctor 모델에서 일부 필드만 가져오도록 설정
        """
        model = models.Doctor
        fields = [
            'id',
            'name',
            'office_name',
            'specialties',
            'non_reimbursable',
            'opening_hours',
        ]


class CreateAppointmentSerializer(serializers.ModelSerializer):
    """
    진료 요청을 하는 시리얼라이저, 뷰 대신에 시리얼라이저에서
    영업시간, 예약 시간을 검증하게 해보고, expiration도 계산하게
    해보았습니다.
    """

    def validate(self, attrs):
        consultation_datetime = attrs['consultation_datetime']
        weekday = consultation_datetime.weekday() + 1
        time = consultation_datetime.time()
        doctor = attrs['doctor']
        if not doctor.opening_hours.all().exists():
            raise serializers.ValidationError(
                "해당 의사의 영업 시간이 없습니다."
            )
        doctor_qs = get_available_doctors(weekday, time, doctor.id)
        if not doctor_qs.exists():
            raise serializers.ValidationError(
                "예약 시간이 잘못되었습니다. "
                "제대로 된 시간을 넣어주세요."
            )
        return attrs

    def create(self, validated_data):
        the_date = datetime.datetime.now()
        doctor = validated_data['doctor']
        weekday = the_date.weekday() + 1
        time = the_date.time()
        appointment = models.Appointment(
            doctor=doctor,
            patient=validated_data['patient'],
            consultation_datetime=validated_data['consultation_datetime']
        )
        opening_hours = doctor.opening_hours.all()
        delta_15m = datetime.timedelta(minutes=15)
        delta_20m = datetime.timedelta(minutes=20)
        one_day = datetime.timedelta(hours=24)

        opening_hour = opening_hours.filter(weekday=weekday).first()
        if opening_hour:
            if opening_hour.lunch_hour is not None and opening_hour.lunch_hour <= time and opening_hour.lunch_end_hour >= time:
                appointment.expiration = datetime.datetime.combine(
                    the_date.date(), opening_hour.lunch_end_hour) + delta_15m
                appointment.save()
                return appointment
            if opening_hour.from_hour <= time and opening_hour.to_hour >= time:
                appointment.expiration = the_date + delta_20m
                appointment.save()
                return appointment
            if opening_hour.from_hour > time:
                appointment.expiration = datetime.datetime.combine(
                    the_date.date(), opening_hour.from_hour) + delta_15m
                appointment.save()
                return appointment

        weekday = weekday % 7 + 1
        the_date = the_date + one_day

        while True:
            opening_hour = opening_hours.filter(weekday=weekday).first()
            if opening_hour:
                appointment.expiration = datetime.datetime.combine(
                    the_date.date(), opening_hour.from_hour) + delta_15m
                appointment.save()
                return appointment

            weekday = weekday % 7 + 1
            the_date = the_date + one_day

    class Meta:
        """
        Appointment 모델과 연동하는 설정.
        """
        model = models.Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'consultation_datetime',
        ]


class InlinePatientSerializer(serializers.ModelSerializer):
    """
    AppointmentSeriailizer에서 환자 정보를 보여주기 위한 용도의 Serialzier
    """
    class Meta:
        """
        Patinet에서 환자 이름만 가져옴.
        """
        model = models.Patient
        fields = [
            'name'
        ]


class AppointmentSerializer(serializers.ModelSerializer):
    """
    진료 요청 정보를 다루는 Serializer
    """
    patient = InlinePatientSerializer()

    class Meta:
        """
        Appointment에서 일부 정보를 연동.
        """
        model = models.Appointment
        fields = [
            'id',
            'patient',
            'consultation_datetime',
            'expiration'
        ]
