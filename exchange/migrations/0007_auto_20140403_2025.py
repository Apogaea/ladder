# encoding: utf8
from django.db import models, migrations
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_auto_20140331_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ladderprofile',
            name='phone_number',
            field=localflavor.us.models.PhoneNumberField(help_text=u'US Phone Number (XXX-XXX-XXXX)', unique=True, max_length=20, verbose_name='Phone Number'),
        ),
    ]
