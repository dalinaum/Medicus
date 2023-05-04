from django.contrib import admin
from .models import Doctor, MedicalSpecialty, Patient


admin.site.register(Patient)
admin.site.register(MedicalSpecialty)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_name', 'specialties_in_one_line', 'non_reimbursable']


    @staticmethod
    def specialties_in_one_line(doctor):
        return ", ".join(str(v) for v in doctor.specialties.all())
