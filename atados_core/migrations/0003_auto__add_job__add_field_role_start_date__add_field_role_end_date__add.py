# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table(u'atados_core_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Project'], unique=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Job'])

        # Adding M2M table for field skills on 'Job'
        m2m_table_name = db.shorten_name(u'atados_core_job_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm[u'atados_core.job'], null=False)),
            ('skill', models.ForeignKey(orm[u'atados_core.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['job_id', 'skill_id'])

        # Adding field 'Role.start_date'
        db.add_column(u'atados_core_role', 'start_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.end_date'
        db.add_column(u'atados_core_role', 'end_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Role.job'
        db.add_column(u'atados_core_role', 'job',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.datetime(2013, 10, 28, 0, 0), to=orm['atados_core.Job']),
                      keep_default=False)

        # Adding field 'Nonprofit.created_date'
        db.add_column(u'atados_core_nonprofit', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Nonprofit.last_modified_date'
        db.add_column(u'atados_core_nonprofit', 'last_modified_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.facebook_event'
        db.add_column(u'atados_core_project', 'facebook_event',
                      self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.created_date'
        db.add_column(u'atados_core_project', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.last_modified_date'
        db.add_column(u'atados_core_project', 'last_modified_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.created_date'
        db.add_column(u'atados_core_volunteer', 'created_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Volunteer.last_modified_date'
        db.add_column(u'atados_core_volunteer', 'last_modified_date',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2013, 10, 28, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Apply.role'
        db.add_column(u'atados_core_apply', 'role',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=datetime.datetime(2013, 10, 28, 0, 0), to=orm['atados_core.Role']),
                      keep_default=False)

        # Adding field 'Apply.canceled'
        db.add_column(u'atados_core_apply', 'canceled',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Apply.canceled_date'
        db.add_column(u'atados_core_apply', 'canceled_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Job'
        db.delete_table(u'atados_core_job')

        # Removing M2M table for field skills on 'Job'
        db.delete_table(db.shorten_name(u'atados_core_job_skills'))

        # Deleting field 'Role.start_date'
        db.delete_column(u'atados_core_role', 'start_date')

        # Deleting field 'Role.end_date'
        db.delete_column(u'atados_core_role', 'end_date')

        # Deleting field 'Role.job'
        db.delete_column(u'atados_core_role', 'job_id')

        # Deleting field 'Nonprofit.created_date'
        db.delete_column(u'atados_core_nonprofit', 'created_date')

        # Deleting field 'Nonprofit.last_modified_date'
        db.delete_column(u'atados_core_nonprofit', 'last_modified_date')

        # Deleting field 'Project.facebook_event'
        db.delete_column(u'atados_core_project', 'facebook_event')

        # Deleting field 'Project.created_date'
        db.delete_column(u'atados_core_project', 'created_date')

        # Deleting field 'Project.last_modified_date'
        db.delete_column(u'atados_core_project', 'last_modified_date')

        # Deleting field 'Volunteer.created_date'
        db.delete_column(u'atados_core_volunteer', 'created_date')

        # Deleting field 'Volunteer.last_modified_date'
        db.delete_column(u'atados_core_volunteer', 'last_modified_date')

        # Deleting field 'Apply.role'
        db.delete_column(u'atados_core_apply', 'role_id')

        # Deleting field 'Apply.canceled'
        db.delete_column(u'atados_core_apply', 'canceled')

        # Deleting field 'Apply.canceled_date'
        db.delete_column(u'atados_core_apply', 'canceled_date')


    models = {
        u'atados_core.address': {
            'Meta': {'object_name': 'Address'},
            'addressline': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressline2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressnumber': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.City']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.State']", 'null': 'True', 'blank': 'True'}),
            'suburb': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.Suburb']", 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.apply': {
            'Meta': {'object_name': 'Apply'},
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Project']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Role']"}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Volunteer']"})
        },
        u'atados_core.availability': {
            'Meta': {'object_name': 'Availability'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
        u'atados_core.donation': {
            'Meta': {'object_name': 'Donation'},
            'collection_by_nonprofit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delivery': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Project']", 'unique': 'True'})
        },
        u'atados_core.job': {
            'Meta': {'object_name': 'Job'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Project']", 'unique': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Skill']", 'symmetrical': 'False'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'atados_core.material': {
            'Meta': {'object_name': 'Material'},
            'donation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Donation']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'quantity': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.nonprofit': {
            'Meta': {'object_name': 'Nonprofit'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Cause']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google_page': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '51', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'nonprofit_created_by'", 'to': u"orm['auth.User']"})
        },
        u'atados_core.project': {
            'Meta': {'object_name': 'Project'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Cause']", 'symmetrical': 'False'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook_event': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nonprofit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Nonprofit']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsible': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'atados_core.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.City']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Project']"}),
            'sort': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.State']", 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.role': {
            'Meta': {'object_name': 'Role'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prerequisites': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vacancies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'work': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Work']"})
        },
        u'atados_core.skill': {
            'Meta': {'object_name': 'Skill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.state': {
            'Meta': {'object_name': 'State'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.suburb': {
            'Meta': {'object_name': 'Suburb'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'atados_core.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Cause']", 'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'facebook_access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'facebook_access_token_expires': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_uid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'last_modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Skill']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'atados_core.work': {
            'Meta': {'object_name': 'Work'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True'}),
            'availabilities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Availability']", 'symmetrical': 'False'}),
            'can_be_done_remotely': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Project']", 'unique': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Skill']", 'symmetrical': 'False'}),
            'weekly_hours': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
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

    complete_apps = ['atados_core']