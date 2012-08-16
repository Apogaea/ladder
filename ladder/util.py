import datetime
from django.utils.timezone import utc

now = lambda: datetime.datetime.utcnow().replace(tzinfo=utc)
