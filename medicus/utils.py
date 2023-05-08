from django.db.models import Q
from .models import Doctor


def get_available_doctors_query(weekday, time, doctor_id=None):
    valid_weekday = Q(opening_hours__weekday=weekday)
    valid_opening_hour = Q(
        Q(opening_hours__from_hour__lte=time) &
        Q(opening_hours__to_hour__gte=time)
    )
    not_lunchtime = Q(
        Q(opening_hours__lunch_hour__isnull=True) |
        ~Q(
            Q(opening_hours__lunch_hour__lte=time) &
            Q(opening_hours__lunch_end_hour__gte=time)
        )
    )
    if doctor_id is None:
        return valid_weekday & valid_opening_hour & not_lunchtime
    doctor = Q(id=doctor_id)
    return doctor & valid_weekday & valid_opening_hour & not_lunchtime


def get_available_doctors(weekdays, time, doctor_id=None):
    return Doctor.objects.filter(get_available_doctors_query(weekdays, time, doctor_id))
