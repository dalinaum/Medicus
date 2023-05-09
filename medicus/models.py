from django.db import models
from django.utils.translation import gettext as _

WEEKDAYS = [
    (1, _("Monday")),
    (2, _("Tuesday")),
    (3, _("Wednesday")),
    (4, _("Thursday")),
    (5, _("Friday")),
    (6, _("Saturday")),
    (7, _("Sunday")),
]


class Patient(models.Model):
    """
    환자 정보를 다루는 모델입니다.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class MedicalSpecialty(models.Model):
    """
    진료과목 정보를 다루는 모델입니다.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Doctor(models.Model):
    """
    의사를 다루는 모델입니다.
    """
    name = models.CharField(max_length=50)
    office_name = models.CharField(max_length=50)
    specialties = models.ManyToManyField(MedicalSpecialty)
    non_reimbursable = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.office_name})"


class OpeningHour(models.Model):
    """
    의사의 영업시간을 다루는 모델입니다.
    """
    doctor = models.ForeignKey(
        Doctor, related_name='opening_hours', on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    lunch_hour = models.TimeField(null=True, blank=True)
    lunch_end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        formatted = f"{self.doctor} {WEEKDAYS[self.weekday - 1][1]} {self.from_hour} ~ {self.to_hour}"
        if self.lunch_hour is None:
            return formatted
        return f"{formatted} (점심 {self.lunch_hour} ~ {self.lunch_end_hour})"

    class Meta:
        """
        영업시간에서 의사와 요일을 함께 유니크로 다룹니다.
        의사는 매일 다른 영업시간을 가집니다.
        """
        unique_together = ('doctor', 'weekday')


class Appointment(models.Model):
    """
    진료요청을 받는 모델입니다.
    진료를 원하는 시간을 의미하는 consultation_datetime이 있고
    요청의 만료 시간인 expiration이 있습니다.
    """
    doctor = models.ForeignKey(
        Doctor, related_name='apointments', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    consultation_datetime = models.DateTimeField()
    accepted = models.BooleanField(default=False)
    accepted_at = models.DateTimeField(blank=True, null=True)
    expiration = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        formatted = f"{self.doctor} {self.patient} {self.consultation_datetime}"
        return formatted
