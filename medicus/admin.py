from django.contrib import admin
from .models import Doctor, MedicalSpecialty, OpeningHour, Patient, Appointment


admin.site.register(Patient)
admin.site.register(MedicalSpecialty)
admin.site.register(OpeningHour)


class OpeningHourInline(admin.TabularInline):
    """
    DoctorAdmin에 영업시간을 포함하기 위한 Inline입니다.
    """
    model = OpeningHour


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Doctor 객체에 대한 Admin 객체입니다. OpeningHours를 inline으로
    포함하고 있습니다.
    """
    list_display = ['name', 'office_name',
                    'specialties_in_one_line', 'non_reimbursable']

    inlines = (OpeningHourInline,)

    @staticmethod
    def specialties_in_one_line(doctor):
        """"
        진료과목을 가져와 한줄의 스트링으로 표현합니다.
        :param doctor: 진료과목을 표현할 의사
        :return 한줄로 정리된 진료 과목
        """
        return ", ".join(str(v) for v in doctor.specialties.all())


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    예약 정보를 가지고 있는 Appointment에 대한 Admin입니다.
    의사, 환자, 예약 정보에 대해 list_display_links로 지정해서
    관리자 모드에서 쉽게 해당 예약을 다룰 수 있게 하였습니다.
    """
    list_display = [
        'doctor',
        'patient',
        'consultation_datetime',
        'accepted',
        'expiration',
    ]
    list_display_links = [
        'doctor',
        'patient',
        'consultation_datetime',
    ]
