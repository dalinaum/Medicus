from rest_framework import serializers
from .models import Doctor, OpeningHour, MedicalSpecialty


class MedicalSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSpecialty
        fields = '__all__'


class OpeningHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpeningHour
        fields = (
            'weekday',
            'from_hour',
            'to_hour',
            'lunch_hour',
            'lunch_end_hour'
        )


class DoctorSereailizer(serializers.ModelSerializer):
    specialties = MedicalSpecialtySerializer(many=True)
    opening_hours = OpeningHourSerializer(many=True)

    class Meta:
        model = Doctor
        fields = (
            "id",
            "name",
            "office_name",
            "specialties",
            "non_reimbursable",
            "opening_hours"
        )
