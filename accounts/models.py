from django.db import models

from fusionbox import behaviors

from authtools.models import AbstractEmailUser


class User(behaviors.Timestampable, AbstractEmailUser):
    display_name = models.CharField('Name', max_length=255, blank=True,
                                    help_text=u"What your name will show up as on the site")

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __unicode__(self):
        return self.display_name
