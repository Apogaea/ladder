# encoding: utf8
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0002_ladderprofile_phonenumber_ticketmatch'),
    ]

    operations = [
        migrations.AddField(
            model_name='ladderprofile',
            name='verified_phone_number',
            field=models.ForeignKey(to_field=u'id', editable=False, to='exchange.PhoneNumber', null=True),
            preserve_default=True,
        ),
    ]
