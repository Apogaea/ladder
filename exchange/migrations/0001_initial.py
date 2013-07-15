# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ('accounts', '0001_initial'),
    )

    def forwards(self, orm):
        # Adding model 'TicketRequest'
        db.create_table(u'exchange_ticketrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='requests', to=orm['accounts.User'])),
            ('message', self.gf('django.db.models.fields.TextField')(max_length=1000)),
            ('is_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_terminated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'exchange', ['TicketRequest'])

        # Adding model 'TicketOffer'
        db.create_table(u'exchange_ticketoffer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='listings', to=orm['accounts.User'])),
            ('is_automatch', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_cancelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_terminated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'exchange', ['TicketOffer'])

        # Adding model 'TicketMatch'
        db.create_table(u'exchange_ticketmatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('ticket_request', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['exchange.TicketRequest'])),
            ('ticket_offer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['exchange.TicketOffer'])),
            ('expires_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 16, 0, 0))),
            ('is_accepted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_terminated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'exchange', ['TicketMatch'])

        # Adding model 'LadderProfile'
        db.create_table(u'exchange_ladderprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='ladder_profile', unique=True, to=orm['accounts.User'])),
            ('phone_number', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20)),
            ('verified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'exchange', ['LadderProfile'])

        # Adding model 'PhoneNumber'
        db.create_table(u'exchange_phonenumber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='codes', to=orm['exchange.LadderProfile'])),
            ('phone_number', self.gf('django_localflavor_us.models.PhoneNumberField')(max_length=20, blank=True)),
            ('confirmation_code', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('attempts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('last_sent_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'exchange', ['PhoneNumber'])


    def backwards(self, orm):
        # Deleting model 'TicketRequest'
        db.delete_table(u'exchange_ticketrequest')

        # Deleting model 'TicketOffer'
        db.delete_table(u'exchange_ticketoffer')

        # Deleting model 'TicketMatch'
        db.delete_table(u'exchange_ticketmatch')

        # Deleting model 'LadderProfile'
        db.delete_table(u'exchange_ladderprofile')

        # Deleting model 'PhoneNumber'
        db.delete_table(u'exchange_phonenumber')


    models = {
        u'accounts.user': {
            'Meta': {'object_name': 'User'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'exchange.ladderprofile': {
            'Meta': {'object_name': 'LadderProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'ladder_profile'", 'unique': 'True', 'to': u"orm['accounts.User']"}),
            'verified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'exchange.phonenumber': {
            'Meta': {'ordering': "('-last_sent_at',)", 'object_name': 'PhoneNumber'},
            'attempts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'confirmation_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sent_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'phone_number': ('django_localflavor_us.models.PhoneNumberField', [], {'max_length': '20', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'codes'", 'to': u"orm['exchange.LadderProfile']"})
        },
        u'exchange.ticketmatch': {
            'Meta': {'object_name': 'TicketMatch'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 7, 16, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ticket_offer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': u"orm['exchange.TicketOffer']"}),
            'ticket_request': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': u"orm['exchange.TicketRequest']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'exchange.ticketoffer': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'TicketOffer'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_automatch': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'listings'", 'to': u"orm['accounts.User']"})
        },
        u'exchange.ticketrequest': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'TicketRequest'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_terminated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'message': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'requests'", 'to': u"orm['accounts.User']"})
        }
    }

    complete_apps = ['exchange']
