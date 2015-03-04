# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0007_remove_ticketmatch_is_terminated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketoffer',
            name='is_automatch',
        ),
    ]
