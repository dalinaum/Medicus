from rest_framework import serializers
from .models import Doctor, MedicalSpecialty


class MedicalSpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSpecialty
        fields = '__all__'


class DoctorSereailizer(serializers.ModelSerializer):
    specialties = MedicalSpecialtySerializer(many=True)

    class Meta:
        model = Doctor
        fields = ("id", "name", "office_name",
                  "specialties", "non_reimbursable")
