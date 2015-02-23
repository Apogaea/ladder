# encoding: utf8
from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOffer',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_terminated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('is_automatch', models.BooleanField(default=True)),
            ],
            options={
                u'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketRequest',
            fields=[
                (u'id', models.AutoField(verbose_name=u'ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('is_terminated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, to_field=u'id')),
                ('message', models.TextField(max_length=1000)),
            ],
            options={
                u'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
    ]
