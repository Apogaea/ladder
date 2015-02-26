# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0003_auto_20150225_0818'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOfferHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.CharField(max_length=255)),
                ('ticket_offer', models.ForeignKey(related_name='history', to='exchange.TicketOffer')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='ticketrequesthistory',
            options={'ordering': ('-created_at',)},
        ),
    ]
