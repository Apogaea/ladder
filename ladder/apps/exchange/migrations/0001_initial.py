# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LadderProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', localflavor.us.models.PhoneNumberField(help_text='US Phone Number (XXX-XXX-XXXX)', unique=True, max_length=20, verbose_name=b'Phone Number')),
                ('user', models.OneToOneField(related_name='_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accepted_at', models.DateTimeField(null=True)),
                ('is_terminated', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_terminated', models.BooleanField(default=False)),
                ('is_automatch', models.BooleanField(default=True)),
                ('user', models.ForeignKey(related_name='ticket_offers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_terminated', models.BooleanField(default=False)),
                ('message', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(related_name='ticket_requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ticketmatch',
            name='ticket_offer',
            field=models.ForeignKey(related_name='matches', to='exchange.TicketOffer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketmatch',
            name='ticket_request',
            field=models.ForeignKey(related_name='matches', to='exchange.TicketRequest'),
            preserve_default=True,
        ),
    ]
