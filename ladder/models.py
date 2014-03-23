from django.db import models
from django.utils import timezone


class TimestampableModel(models.Model):
    created_at = models.DateTimeField(editable=False, default=timezone.now)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    class Meta:
        abstract = True
