# Medicus

간단한 진료 예약, 검색 API

## 설정

### GitHub Codespace 설정

GitHub Codespace에서 동작할 수 있게 [환경 설정](.devcontainer)이 있습니다. 상단 우측의 `Code` > `Codespaces`를 클릭해 진행할 수 있습니다.

### 로컬 설정

로컬에서 의존성 설정은 `requirements.txt`로 설정합니다.

```python
pip install -r requirements.txt
```

마이그레이션은 다음의 커맨드로 합니다.

```python
python manage.py migrate
```

```python
python manage.py runserver
```
