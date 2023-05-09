# Medicus

간단한 진료 예약, 검색 API

## 설정

### GitHub Codespace 설정

GitHub Codespace에서 동작할 수 있게 [환경 설정](.devcontainer)이 있습니다. GitHub에서 `Code` > `Codespaces`를 클릭해 시작할 수 있습니다.

### 로컬 설정

로컬에서 의존성 설정은 `requirements.txt`로 설정합니다.

```sh
pip install -r requirements.txt
```

마이그레이션은 다음의 커맨드로 합니다.

```sh
python manage.py migrate
```

```sh
python manage.py runserver
```

## 모델

 * `Patient` - 환자 이름을 가지고 있는 모델.
 * `Doctor` - 의사 이름, 진료과목, 비급여 과목을 가지는 모델.
 * `MedicalSpecalty` - 진료 과목의 이름을 가지는 모델.
 * `OpeningHour` - 영업 시간과 점심 시간 정보를 가지는 모델.
 * `Appointment` - 진료 접수 정보, 승락 여부, 만료 시간을 가지는 모델.

[관리자 페이지](/admin)에서 모델의 정보를 다 관리 할 수 있으며 의사 모델(`Doctor`)에서 영업 시간(`OpeningHour`)도 다 설정할 수 있습니다.

## 구현된 API

### 의사 검색

 * 요청 주소: [/medicus/doctor/](/medicus/doctor/)
 * 메서드: GET
 * 쿼리 스트링: search(선택)

`search` 파라미터가 주어지면 해당 파라미터에 맞는 의사를 검색합니다. 주어지지 않았으면 전체 의사를 반환합니다.

### 특정 날짜 시간에 영업중인 의사 검색

 * 요청 주소: [/medicus/doctor/_datetime_/](/medicus/doctor/_datetime_/)
 * 예: [/medicus/doctor/2023-03-11T11:23:33/](/medicus/doctor/2023-03-11T11:23:33/)
 * 메서드: GET

`datetime`에 `%Y-%m-%dT%H:%M:%S` 타입으로 입력된 날짜와 시간을 받아 해당 날짜, 시간에 영업 중인 의사를 반환합니다.

성공했을 때는 다음과 같은 형태로 반환합니다.

```javascript
[
    {
        "id": 2,
        "name": "선재원",
        "office_name": "메라키병원",
        "specialties": [
            {
                "id": 2,
                "name": "한의학과"
            },
            {
                "id": 3,
                "name": "일반의"
            }
        ],
        "non_reimbursable": "다이어트약",
        "opening_hours": [
            {
                "weekday": 1,
                "from_hour": "08:00:00",
                "to_hour": "17:00:00",
                "lunch_hour": "12:00:00",
                "lunch_end_hour": "13:00:00"
            },
            {
                "weekday": 2,
                "from_hour": "08:00:00",
                "to_hour": "17:00:00",
                "lunch_hour": "12:00:00",
                "lunch_end_hour": "13:00:00"
            },
            {
                "weekday": 3,
                "from_hour": "08:00:00",
                "to_hour": "17:00:00",
                "lunch_hour": "12:00:00",
                "lunch_end_hour": "13:00:00"
            },
            {
                "weekday": 4,
                "from_hour": "08:00:00",
                "to_hour": "17:00:00",
                "lunch_hour": "12:00:00",
                "lunch_end_hour": "13:00:00"
            },
            {
                "weekday": 5,
                "from_hour": "08:00:00",
                "to_hour": "17:00:00",
                "lunch_hour": "12:00:00",
                "lunch_end_hour": "13:00:00"
            },
            {
                "weekday": 6,
                "from_hour": "08:00:00",
                "to_hour": "13:00:00",
                "lunch_hour": null,
                "lunch_end_hour": null
            }
        ]
    }
]
```

### 진료 요청

 * 요청 주소: [/medicus/doctor/_doctor_id_/appointment/](/medicus/doctor/_doctor_id_/appointment/)
 * 예: [/medicus/doctor/1/appointment/](/medicus/doctor/1/appointment/)
 * 메서드: POST

요청 파라미터

| 필드                  | 내용                   |
|-----------------------|-----------------------|
| doctor                | 의사의 id              |
| patient               | 환자의 id              |
| consultation_datetime | 진료 요청의 날짜와 시간 |

파라미터의 예

```javascript
{
    "doctor": 1,
    "patient": 3,
    "consultation_datetime": "2023-05-10T10:30:00+09:00"
}
```

의사 id `doctor`, 환자 id `patient`, 진료시간 `consultation_datetime`을 보내어서 요청을 합니다.

성공했을 경우 다음과 같은 형태로 반환합니다.

```javascript
{
    "id": 24,
    "doctor": 1,
    "patient": 3,
    "consultation_datetime": "2023-05-10T10:30:00+09:00"
}
```

잘못된 시간에 예약한 경우 다음과 같이 반환됩니다.

```javascript
{
    "non_field_errors": [
        "예약 시간이 잘못되었습니다. 제대로 된 시간을 넣어주세요."
    ]
}
```

### 진료 요청 확인

 * 요청 주소: [/medicus/doctor/_doctor_id_/pending/](/medicus/doctor/_doctor_id_/pending/)
 * 예: [/medicus/doctor/1/pending/](/medicus/doctor/1/pending/)
 * 메서드: GET

의사에게 온 승인되지 않은 진료 요청을 확인합니다. 성공했을 때는 다음과 같은 형태로 진료 요청을 볼 수 있습니다.

```javascript
[
    {
        "id": 21,
        "patient": {
            "name": "김환자"
        },
        "consultation_datetime": "2023-05-09T10:28:00+09:00",
        "expiration": "2023-05-09T12:15:00+09:00"
    },
    {
        "id": 24,
        "patient": {
            "name": "박환자"
        },
        "consultation_datetime": "2023-05-10T10:30:00+09:00",
        "expiration": "2023-05-10T09:15:00+09:00"
    }
]
```

### 진료 요청 승인

 * 요청 주소: [/medicus/accept_appointment/_appointment_id_/](/medicus/accept_appointment/_appointment_id_/)
 * 예: [/medicus/accept_appointment/21/](/medicus/accept_appointment/21/)
 * 메서드: PATCH

성공했을 때의 예입니다.

별도의 파라미터는 없습니다. 기존의 요청에서 승인 여부만 변경하기 때문에 `PATCH`로 하였습니다.

```javascript
{
    "id": 21,
    "patient": {
        "name": "김환자"
    },
    "consultation_datetime": "2023-05-09T10:28:00+09:00",
    "expiration": "2023-05-09T23:59:29+09:00"
}
```

실패의 예입니다.

```javascript
[
    "진료 요청을 수락할 수 있는 시간이 지났습니다."
]
```
