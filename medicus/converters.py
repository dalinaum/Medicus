from datetime import datetime


class DateTimeConverter:
    """
    라우터에서 사용할 컨버터로 2023-03-11T11:23:33와 같은
    형태로 주소가 오면 datetime으로 파싱합니다.
    """
    regex = '\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}'
    format = '%Y-%m-%dT%H:%M:%S'

    def to_python(self, value):
        """
        주소를 datetime으로 변환합니다.
        :param value: url에서 위치한 값입니다.
        :return datetime으로 변환하여 반환합니다. 
        """
        return datetime.strptime(value, self.format)

    def to_url(self, value):
        """
        datetime을 주소의 형태로 변환합니다.
        :param value: 변환할 datetime
        :return datetime을 주소의 형태로 변환하여 반환합니다.
        """
        return value.strftime(self.format)
