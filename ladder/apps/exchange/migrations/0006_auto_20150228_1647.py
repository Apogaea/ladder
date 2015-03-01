# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0005_ticketoffer_ticket_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketoffer',
            name='ticket_code',
            field=models.CharField(help_text='The TicketFly confirmation code that was given to you when you purchased your ticket', max_length=20),
            preserve_default=True,
        ),
    ]
