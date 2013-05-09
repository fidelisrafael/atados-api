# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Volunteer.zipcode'
        db.add_column('volunteer_volunteer', 'zipcode',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addressline'
        db.add_column('volunteer_volunteer', 'addressline',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.addressnumber'
        db.add_column('volunteer_volunteer', 'addressnumber',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.neighborhood'
        db.add_column('volunteer_volunteer', 'neighborhood',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.state'
        db.add_column('volunteer_volunteer', 'state',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.State'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.city'
        db.add_column('volunteer_volunteer', 'city',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.City'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.suburb'
        db.add_column('volunteer_volunteer', 'suburb',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['core.Suburb'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field causes on 'Volunteer'
        db.create_table('volunteer_volunteer_causes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm['volunteer.volunteer'], null=False)),
            ('cause', models.ForeignKey(orm['core.cause'], null=False))
        ))
        db.create_unique('volunteer_volunteer_causes', ['volunteer_id', 'cause_id'])

        # Adding M2M table for field skills on 'Volunteer'
        db.create_table('volunteer_volunteer_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm['volunteer.volunteer'], null=False)),
            ('skill', models.ForeignKey(orm['core.skill'], null=False))
        ))
        db.create_unique('volunteer_volunteer_skills', ['volunteer_id', 'skill_id'])


    def backwards(self, orm):
        # Deleting field 'Volunteer.zipcode'
        db.delete_column('volunteer_volunteer', 'zipcode')

        # Deleting field 'Volunteer.addressline'
        db.delete_column('volunteer_volunteer', 'addressline')

        # Deleting field 'Volunteer.addressnumber'
        db.delete_column('volunteer_volunteer', 'addressnumber')

        # Deleting field 'Volunteer.neighborhood'
        db.delete_column('volunteer_volunteer', 'neighborhood')

        # Deleting field 'Volunteer.state'
        db.delete_column('volunteer_volunteer', 'state_id')

        # Deleting field 'Volunteer.city'
        db.delete_column('volunteer_volunteer', 'city_id')

        # Deleting field 'Volunteer.suburb'
        db.delete_column('volunteer_volunteer', 'suburb_id')

        # Removing M2M table for field causes on 'Volunteer'
        db.delete_table('volunteer_volunteer_causes')

        # Removing M2M table for field skills on 'Volunteer'
        db.delete_table('volunteer_volunteer_skills')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.cause': {
            'Meta': {'object_name': 'Cause'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.State']"})
        },
        'core.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'core.suburb': {
            'Meta': {'object_name': 'Suburb'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.City']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'volunteer.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'addressline': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressnumber': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Cause']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['core.City']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Skill']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['core.State']", 'null': 'True', 'blank': 'True'}),
            'suburb': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['core.Suburb']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['volunteer']