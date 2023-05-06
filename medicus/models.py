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
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class MedicalSpecialty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Doctor(models.Model):
    name = models.CharField(max_length=50)
    office_name = models.CharField(max_length=50)
    specialties = models.ManyToManyField(MedicalSpecialty)
    non_reimbursable = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} ({self.office_name})"


class OpeningHour(models.Model):
    doctor = models.ForeignKey(Doctor, related_name='opening_hours', on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAYS)
    from_hour = models.TimeField()
    to_hour = models.TimeField()
    lunch_hour = models.TimeField(null=True, blank=True)
    lunch_end_hour = models.TimeField(null=True, blank=True)

    def __str__(self):
        formatted = f"{self.doctor} {self.from_hour} ~ {self.to_hour}"
        if self.lunch_hour is None:
            return formatted
        return f"{formatted} (점심 {self.lunch_hour} ~ {self.lunch_end_hour})"

    class Meta:
        unique_together = ('doctor', 'weekday') 
