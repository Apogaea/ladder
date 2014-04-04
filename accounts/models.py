from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from authtools.models import AbstractEmailUser

from ladder.models import TimestampableModel


class User(TimestampableModel, AbstractEmailUser):
    display_name = models.CharField('Name', max_length=255, blank=True,
                                    help_text=u"What your name will show up as on the site")

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __unicode__(self):
        return self.display_name

    @property
    def profile(self):
        try:
            return self._profile
        except ObjectDoesNotExist:
            from exchange.models import LadderProfile
            return LadderProfile.objects.get_or_create(user=self)[0]

    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser
