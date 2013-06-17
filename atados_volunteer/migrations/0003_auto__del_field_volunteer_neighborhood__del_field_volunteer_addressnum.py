# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Volunteer.neighborhood'
        db.delete_column(u'atados_volunteer_volunteer', 'neighborhood')

        # Deleting field 'Volunteer.addressnumber'
        db.delete_column(u'atados_volunteer_volunteer', 'addressnumber')

        # Deleting field 'Volunteer.city'
        db.delete_column(u'atados_volunteer_volunteer', 'city_id')

        # Deleting field 'Volunteer.addressline'
        db.delete_column(u'atados_volunteer_volunteer', 'addressline')

        # Deleting field 'Volunteer.suburb'
        db.delete_column(u'atados_volunteer_volunteer', 'suburb_id')

        # Deleting field 'Volunteer.zipcode'
        db.delete_column(u'atados_volunteer_volunteer', 'zipcode')

        # Deleting field 'Volunteer.state'
        db.delete_column(u'atados_volunteer_volunteer', 'state_id')

        # Adding field 'Volunteer.address'
        db.add_column(u'atados_volunteer_volunteer', 'address',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Volunteer.neighborhood'
        db.add_column(u'atados_volunteer_volunteer', 'neighborhood',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addressnumber'
        db.add_column(u'atados_volunteer_volunteer', 'addressnumber',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.city'
        db.add_column(u'atados_volunteer_volunteer', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.City'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addressline'
        db.add_column(u'atados_volunteer_volunteer', 'addressline',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.suburb'
        db.add_column(u'atados_volunteer_volunteer', 'suburb',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.Suburb'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.zipcode'
        db.add_column(u'atados_volunteer_volunteer', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.state'
        db.add_column(u'atados_volunteer_volunteer', 'state',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.State'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Volunteer.address'
        db.delete_column(u'atados_volunteer_volunteer', 'address_id')


    models = {
        u'atados_core.address': {
            'Meta': {'object_name': 'Address'},
            'addressline': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressnumber': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.City']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.State']", 'null': 'True', 'blank': 'True'}),
            'suburb': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.Suburb']", 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.cause': {
            'Meta': {'object_name': 'Cause'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.State']"})
        },
        u'atados_core.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.state': {
            'Meta': {'object_name': 'State'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.suburb': {
            'Meta': {'object_name': 'Suburb'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_volunteer.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Cause']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Skill']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['atados_volunteer']