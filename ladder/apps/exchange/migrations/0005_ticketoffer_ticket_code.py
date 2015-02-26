# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0004_auto_20150225_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketoffer',
            name='ticket_code',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
