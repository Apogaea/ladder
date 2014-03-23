# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0005_auto_20140330_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ladderprofile',
            name='verified_phone_number',
        ),
        migrations.DeleteModel(
            name='PhoneNumber',
        ),
    ]
