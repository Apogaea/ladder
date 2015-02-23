# encoding: utf8
from django.db import models, migrations
import localflavor.us.models


def remove_duplicate_phone_numbers(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    LadderProfile = apps.get_model("exchange", "LadderProfile")
    phone_numbers = LadderProfile.objects.values_list('phone_number', flat=True)

    for phone_number in phone_numbers:
        profiles = LadderProfile.objects.order_by('pk').filter(phone_number=phone_number)
        to_delete = profiles[1:].values_list('pk', flat=True)
        LadderProfile.objects.filter(pk__in=to_delete).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_auto_20140331_1759'),
    ]

    operations = [
        migrations.RunPython(remove_duplicate_phone_numbers),
        migrations.AlterField(
            model_name='ladderprofile',
            name='phone_number',
            field=localflavor.us.models.PhoneNumberField(help_text=u'US Phone Number (XXX-XXX-XXXX)', unique=True, max_length=20, verbose_name='Phone Number'),
        ),
    ]
