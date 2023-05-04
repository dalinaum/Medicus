from django.db import models


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