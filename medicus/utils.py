"""진료 가능한 의사를 찾는 함수들"""
from django.db.models import Q
from .models import Doctor


def get_available_doctors_query(weekday, time, doctor_id=None):
    """
    진료가능한 의사를 찾는 쿼리를 만듭니다.

    :param weekday: 진료를 원하는 요일. 숫자 값.
    :param time: 진료를 원하는 시간.
    :doctor_id: 진료를 원하는 의사. (선택)
    :return 진료가능한 의사를 찾는 쿼리를 반환합니다.
    """
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


def get_available_doctors(weekday, time, doctor_id=None):
    """
    진료가능한 의사를 찾습니다.

    :param weekday: 진료를 원하는 요일. 숫자 값.
    :param time: 진료를 원하는 시간.
    :doctor_id: 진료를 원하는 의사. (선택)
    :return 진료가능한 의사들을 반환합니다.
    """
    return Doctor.objects.filter(get_available_doctors_query(weekday, time, doctor_id))
