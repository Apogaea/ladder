# encoding: utf8
from django.db import models, migrations


def delete_users_with_bad_phone_numbers(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.

    User = apps.get_model("accounts", "User")
    User.objects.filter(ladderprofile__isnull=True).delete()
    User.objects.filter(ladderprofile__phone_number='').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0007_auto_20140403_2025'),
    ]

    operations = [
        migrations.RunPython(delete_users_with_bad_phone_numbers),
    ]
