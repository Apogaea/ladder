from django.db import models

from django_localflavor_us import models as us_models

from fusionbox import behaviors

from authtools.models import AbstractEmailUser


class User(behaviors.QuerySetManagerModel, behaviors.Timestampable, AbstractEmailUser):
    display_name = models.CharField(max_length=255, blank=True,
                                    help_text=u"What your name will show up as on the site")

    phone_number = us_models.PhoneNumberField("Phone Number", max_length=255,
                                              help_text=u"US Phone Number (XXX-XXX-XXXX)")
    is_verified = models.BooleanField(blank=True, default=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    def get_full_name(self):
        return self.display_name

    def get_short_name(self):
        return self.display_name

    def __unicode__(self):
        return self.display_name

    #|
    #|  Permission Shortcuts
    #|
    @property
    def can_list_ticket(self):
        if not self.is_verified:
            return False
        if self.requests.active().exists():
            return False
        return True

    @property
    def can_request_ticket(self):
        if not self.is_verified:
            return False
        if self.listings.active().exists():
            return False
        return True
