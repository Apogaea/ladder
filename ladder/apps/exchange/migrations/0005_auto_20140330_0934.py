# encoding: utf8
from django.db import models, migrations


def move_phone_numbers_to_profile(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    LadderProfile = apps.get_model("exchange", "LadderProfile")
    for profile in LadderProfile.objects.filter(verified_phone_number__isnull=False):
        profile.phone_number = profile.verified_phone_number.phone_number
        profile.save()

    LadderProfile.objects.filter(verified_phone_number__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_ladderprofile_phone_number'),
    ]

    operations = [
        migrations.RunPython(move_phone_numbers_to_profile),
    ]
