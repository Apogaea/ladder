from django.db import models

from fusionbox import behaviors

from authtools.models import AbstractEmailUser


class User(behaviors.QuerySetManagerModel, behaviors.Timestampable, AbstractEmailUser):
    display_name = models.CharField(max_length=255, blank=True,
            help_text=u"What your name will show up as on the site")
