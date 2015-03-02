# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_auto_20150228_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketmatch',
            name='is_terminated',
        ),
    ]
