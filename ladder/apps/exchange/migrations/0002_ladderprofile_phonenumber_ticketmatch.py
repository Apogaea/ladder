# encoding: utf8
from django.db import models, migrations
import exchange.models
import django.utils.timezone
from django.conf import settings
import localflavor.us.models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketMatch',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ticket_request', models.ForeignKey(to='exchange.TicketRequest', to_field=u'id')),
                ('ticket_offer', models.ForeignKey(to='exchange.TicketOffer', to_field=u'id')),
                ('accepted_at', models.DateTimeField(null=True)),
                ('is_terminated', models.BooleanField(default=False)),
            ],
            options={
                u'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LadderProfile',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, to_field=u'id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('profile', models.ForeignKey(to='exchange.LadderProfile', to_field=u'id')),
                ('phone_number', localflavor.us.models.PhoneNumberField(help_text=u'US Phone Number (XXX-XXX-XXXX)', max_length=20, verbose_name='Phone Number')),
                ('verified_at', models.DateTimeField(null=True, editable=False)),
                ('confirmation_code', models.CharField(default='', max_length=255, editable=False, blank=True)),
                ('attempts', models.PositiveIntegerField(default=0, blank=True)),
                ('last_sent_at', models.DateTimeField(null=True, editable=False, blank=True)),
            ],
            options={
                u'ordering': ('-last_sent_at',),
                u'get_latest_by': 'created_at',
            },
            bases=(models.Model,),
        ),
    ]
