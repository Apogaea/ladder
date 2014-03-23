# encoding: utf8
from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_ladderprofile_verified_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='ladderprofile',
            name='phone_number',
            field=localflavor.us.models.PhoneNumberField(default='', help_text=u'US Phone Number (XXX-XXX-XXXX)', max_length=20, verbose_name='Phone Number'),
            preserve_default=False,
        ),
    ]
