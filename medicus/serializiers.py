import datetime
from rest_framework import serializers
from . import models
from .utils import get_available_doctors


class MedicalSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MedicalSpecialty
        fields = '__all__'


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OpeningHour
        fields = [
            'weekday',
            'from_hour',
            'to_hour',
            'lunch_hour',
            'lunch_end_hour'
        ]


class DoctorSereailizer(serializers.ModelSerializer):
    specialties = MedicalSpecialtySerializer(many=True)
    opening_hours = OpeningHourSerializer(many=True)

    class Meta:
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
        model = models.Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'consultation_datetime',
        ]
        read_only_fields = [
            'read_only_fields'
        ]
