# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Account.subscribed_to_news'
        db.add_column('accounts', 'subscribed_to_news',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Account.subscribed_to_news'
        db.delete_column('accounts', 'subscribed_to_news')


    models = {
        u'core.account': {
            'Meta': {'object_name': 'Account', 'db_table': "'accounts'"},
            'company_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'account-bamv2xy3z948uhiw'", 'max_length': '24', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Service']", 'null': 'True', 'symmetrical': 'False'}),
            'subscribed_to_news': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'core.plan': {
            'Meta': {'object_name': 'Plan', 'db_table': "'plans'"},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'plan-8abh6ns2j0pfyr9q'", 'max_length': '24', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service', 'db_table': "'services'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'service-itae3nrdk802xfvw'", 'max_length': '24', 'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Plan']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['core']