# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_ladderprofile_max_allowed_matches'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketRequestHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=255)),
                ('ticket_request', models.ForeignKey(related_name='history', to='exchange.TicketRequest')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='ticketrequest',
            name='message',
            field=models.TextField(max_length=200),
            preserve_default=True,
        ),
    ]
