# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ladderprofile',
            name='max_allowed_matches',
            field=models.PositiveIntegerField(default=2, blank=True),
            preserve_default=True,
        ),
    ]
