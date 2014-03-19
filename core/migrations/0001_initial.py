# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plan'
        db.create_table('plans', (
            ('id', self.gf('django.db.models.fields.CharField')(default='plan-wa4htn9v1b738jzl', max_length=24, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('capacity', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'core', ['Plan'])

        # Adding model 'Service'
        db.create_table('services', (
            ('id', self.gf('django.db.models.fields.CharField')(default='service-yxo0edhki9msvbna', max_length=24, primary_key=True)),
            ('plan', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Plan'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=10)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('users', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('hostname', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding model 'Account'
        db.create_table('accounts', (
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.CharField')(default='account-4hn1kaiqxjtz25fp', max_length=24, primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('company_address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('joined_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Account'])

        # Adding M2M table for field services on 'Account'
        m2m_table_name = db.shorten_name('accounts_services')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('account', models.ForeignKey(orm[u'core.account'], null=False)),
            ('service', models.ForeignKey(orm[u'core.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['account_id', 'service_id'])


    def backwards(self, orm):
        # Deleting model 'Plan'
        db.delete_table('plans')

        # Deleting model 'Service'
        db.delete_table('services')

        # Deleting model 'Account'
        db.delete_table('accounts')

        # Removing M2M table for field services on 'Account'
        db.delete_table(db.shorten_name('accounts_services'))


    models = {
        u'core.account': {
            'Meta': {'object_name': 'Account', 'db_table': "'accounts'"},
            'company_address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'account-5d9n8gzrwx0sh2y7'", 'max_length': '24', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Service']", 'null': 'True', 'symmetrical': 'False'})
        },
        u'core.plan': {
            'Meta': {'object_name': 'Plan', 'db_table': "'plans'"},
            'capacity': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'plan-u62cg9a3w1e4bsjy'", 'max_length': '24', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service', 'db_table': "'services'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hostname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'service-ligvhqsnc4ob351y'", 'max_length': '24', 'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Plan']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '10'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'users': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['core']