from django.contrib import admin
from .models import Doctor, MedicalSpecialty, OpeningHour, Patient


admin.site.register(Patient)
admin.site.register(MedicalSpecialty)
admin.site.register(OpeningHour)


class OpeningHourInline(admin.TabularInline):
    model = OpeningHour


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_name',
                    'specialties_in_one_line', 'non_reimbursable']

    inlines = (OpeningHourInline,)

    @staticmethod
    def specialties_in_one_line(doctor):
        return ", ".join(str(v) for v in doctor.specialties.all())
