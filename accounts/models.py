from django.db import models
from django.contrib.auth.models import User as DjangoUser, UserManager as DjangoUserManager

from fusionbox import behaviors
from fusionbox.db.models import QuerySetManager


class UserManager(QuerySetManager, DjangoUserManager):
    pass


class User(behaviors.QuerySetManagerModel, DjangoUser):
    preferred_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=255)

    is_verified = models.BooleanField(blank=True, default=False)
    verified_at = models.DateTimeField(blank=True, null=True)

    objects = UserManager()
