import datetime
import time

from django.utils import timezone


def test_frozen_now_util(frozen_now):
    now_tz = timezone.now()
    now_dt = datetime.datetime.now()
    now_time = time.time()
    today = datetime.date.today()

    time.sleep(1)

    _now_tz = timezone.now()
    _now_dt = datetime.datetime.now()
    _now_time = time.time()
    _today = datetime.date.today()

    assert now_tz == _now_tz
    assert now_dt == _now_dt
    assert now_time == _now_time
    assert today == _today
