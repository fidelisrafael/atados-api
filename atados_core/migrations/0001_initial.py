# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Availability'
        db.create_table(u'atados_core_availability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weekday', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('period', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'atados_core', ['Availability'])

        # Adding model 'Cause'
        db.create_table(u'atados_core_cause', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'atados_core', ['Cause'])

        # Adding model 'Skill'
        db.create_table(u'atados_core_skill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'atados_core', ['Skill'])

        # Adding model 'State'
        db.create_table(u'atados_core_state', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'atados_core', ['State'])

        # Adding model 'City'
        db.create_table(u'atados_core_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.State'])),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'atados_core', ['City'])

        # Adding model 'Address'
        db.create_table(u'atados_core_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('addressline', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('addressnumber', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('addressline2', self.gf('django.db.models.fields.CharField')(default=None, max_length=100, null=True, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.City'], null=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Address'])

        # Adding model 'Volunteer'
        db.create_table(u'atados_core_volunteer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.User'], unique=True)),
            ('facebook_uid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_access_token', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('facebook_access_token_expires', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Volunteer'])

        # Adding M2M table for field causes on 'Volunteer'
        m2m_table_name = db.shorten_name(u'atados_core_volunteer_causes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm[u'atados_core.volunteer'], null=False)),
            ('cause', models.ForeignKey(orm[u'atados_core.cause'], null=False))
        ))
        db.create_unique(m2m_table_name, ['volunteer_id', 'cause_id'])

        # Adding M2M table for field skills on 'Volunteer'
        m2m_table_name = db.shorten_name(u'atados_core_volunteer_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('volunteer', models.ForeignKey(orm[u'atados_core.volunteer'], null=False)),
            ('skill', models.ForeignKey(orm[u'atados_core.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['volunteer_id', 'skill_id'])

        # Adding model 'Nonprofit'
        db.create_table(u'atados_core_nonprofit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.User'], unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('details', self.gf('django.db.models.fields.TextField')(default=None, max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('facebook_page', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('google_page', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(default=None, max_length=51, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Nonprofit'])

        # Adding M2M table for field causes on 'Nonprofit'
        m2m_table_name = db.shorten_name(u'atados_core_nonprofit_causes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nonprofit', models.ForeignKey(orm[u'atados_core.nonprofit'], null=False)),
            ('cause', models.ForeignKey(orm[u'atados_core.cause'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nonprofit_id', 'cause_id'])

        # Adding M2M table for field volunteers on 'Nonprofit'
        m2m_table_name = db.shorten_name(u'atados_core_nonprofit_volunteers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('nonprofit', models.ForeignKey(orm[u'atados_core.nonprofit'], null=False)),
            ('volunteer', models.ForeignKey(orm[u'atados_core.volunteer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['nonprofit_id', 'volunteer_id'])

        # Adding model 'Role'
        db.create_table(u'atados_core_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('prerequisites', self.gf('django.db.models.fields.TextField')(default=None, max_length=1024, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(default=None, max_length=1024, null=True, blank=True)),
            ('vacancies', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Role'])

        # Adding model 'Project'
        db.create_table(u'atados_core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nonprofit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Nonprofit'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('details', self.gf('django.db.models.fields.TextField')(max_length=3000)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('facebook_event', self.gf('django.db.models.fields.URLField')(default=None, max_length=200, null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('published_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True, null=True, blank=True)),
            ('legacy_nid', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Project'])

        # Adding M2M table for field roles on 'Project'
        m2m_table_name = db.shorten_name(u'atados_core_project_roles')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'atados_core.project'], null=False)),
            ('role', models.ForeignKey(orm[u'atados_core.role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'role_id'])

        # Adding M2M table for field skills on 'Project'
        m2m_table_name = db.shorten_name(u'atados_core_project_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'atados_core.project'], null=False)),
            ('skill', models.ForeignKey(orm[u'atados_core.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'skill_id'])

        # Adding M2M table for field causes on 'Project'
        m2m_table_name = db.shorten_name(u'atados_core_project_causes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'atados_core.project'], null=False)),
            ('cause', models.ForeignKey(orm[u'atados_core.cause'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'cause_id'])

        # Adding model 'Work'
        db.create_table(u'atados_core_work', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Project'], unique=True)),
            ('weekly_hours', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('can_be_done_remotely', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'atados_core', ['Work'])

        # Adding M2M table for field availabilities on 'Work'
        m2m_table_name = db.shorten_name(u'atados_core_work_availabilities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('work', models.ForeignKey(orm[u'atados_core.work'], null=False)),
            ('availability', models.ForeignKey(orm[u'atados_core.availability'], null=False))
        ))
        db.create_unique(m2m_table_name, ['work_id', 'availability_id'])

        # Adding model 'Job'
        db.create_table(u'atados_core_job', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Project'], unique=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Job'])

        # Adding model 'ApplyStatus'
        db.create_table(u'atados_core_applystatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'atados_core', ['ApplyStatus'])

        # Adding model 'Apply'
        db.create_table(u'atados_core_apply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Volunteer'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Project'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('canceled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('canceled_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Apply'])

        # Adding model 'Recommendation'
        db.create_table(u'atados_core_recommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Project'])),
            ('sort', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.State'], null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.City'], null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Recommendation'])

        # Adding model 'User'
        db.create_table(u'atados_core_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_email_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('joined_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('legacy_uid', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['User'])


    def backwards(self, orm):
        # Deleting model 'Availability'
        db.delete_table(u'atados_core_availability')

        # Deleting model 'Cause'
        db.delete_table(u'atados_core_cause')

        # Deleting model 'Skill'
        db.delete_table(u'atados_core_skill')

        # Deleting model 'State'
        db.delete_table(u'atados_core_state')

        # Deleting model 'City'
        db.delete_table(u'atados_core_city')

        # Deleting model 'Address'
        db.delete_table(u'atados_core_address')

        # Deleting model 'Volunteer'
        db.delete_table(u'atados_core_volunteer')

        # Removing M2M table for field causes on 'Volunteer'
        db.delete_table(db.shorten_name(u'atados_core_volunteer_causes'))

        # Removing M2M table for field skills on 'Volunteer'
        db.delete_table(db.shorten_name(u'atados_core_volunteer_skills'))

        # Deleting model 'Nonprofit'
        db.delete_table(u'atados_core_nonprofit')

        # Removing M2M table for field causes on 'Nonprofit'
        db.delete_table(db.shorten_name(u'atados_core_nonprofit_causes'))

        # Removing M2M table for field volunteers on 'Nonprofit'
        db.delete_table(db.shorten_name(u'atados_core_nonprofit_volunteers'))

        # Deleting model 'Role'
        db.delete_table(u'atados_core_role')

        # Deleting model 'Project'
        db.delete_table(u'atados_core_project')

        # Removing M2M table for field roles on 'Project'
        db.delete_table(db.shorten_name(u'atados_core_project_roles'))

        # Removing M2M table for field skills on 'Project'
        db.delete_table(db.shorten_name(u'atados_core_project_skills'))

        # Removing M2M table for field causes on 'Project'
        db.delete_table(db.shorten_name(u'atados_core_project_causes'))

        # Deleting model 'Work'
        db.delete_table(u'atados_core_work')

        # Removing M2M table for field availabilities on 'Work'
        db.delete_table(db.shorten_name(u'atados_core_work_availabilities'))

        # Deleting model 'Job'
        db.delete_table(u'atados_core_job')

        # Deleting model 'ApplyStatus'
        db.delete_table(u'atados_core_applystatus')

        # Deleting model 'Apply'
        db.delete_table(u'atados_core_apply')

        # Deleting model 'Recommendation'
        db.delete_table(u'atados_core_recommendation')

        # Deleting model 'User'
        db.delete_table(u'atados_core_user')


    models = {
        u'atados_core.address': {
            'Meta': {'object_name': 'Address'},
            'addressline': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'addressline2': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'addressnumber': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['atados_core.City']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.apply': {
            'Meta': {'object_name': 'Apply'},
            'canceled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'canceled_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Project']"}),
            'volunteer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Volunteer']"})
        },
        u'atados_core.applystatus': {
            'Meta': {'object_name': 'ApplyStatus'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.State']"})
        },
        u'atados_core.job': {
            'Meta': {'object_name': 'Job'},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Project']", 'unique': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'atados_core.nonprofit': {
            'Meta': {'object_name': 'Nonprofit'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Cause']", 'null': 'True', 'blank': 'True'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'facebook_page': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'google_page': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '51', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.User']", 'unique': 'True'}),
            'volunteers': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Volunteer']", 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'atados_core.project': {
            'Meta': {'object_name': 'Project'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Cause']", 'symmetrical': 'False'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closed_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'facebook_event': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'legacy_nid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nonprofit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Nonprofit']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'responsible': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Role']", 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Skill']", 'symmetrical': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
            'details': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prerequisites': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'vacancies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
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
        u'atados_core.user': {
            'Meta': {'object_name': 'User'},
            'address': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Address']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'legacy_uid': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'atados_core.volunteer': {
            'Meta': {'object_name': 'Volunteer'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Cause']", 'null': 'True', 'blank': 'True'}),
            'facebook_access_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'facebook_access_token_expires': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook_uid': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['atados_core.Skill']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.User']", 'unique': 'True'})
        },
        u'atados_core.work': {
            'Meta': {'object_name': 'Work'},
            'availabilities': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Availability']", 'symmetrical': 'False'}),
            'can_be_done_remotely': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['atados_core.Project']", 'unique': 'True'}),
            'weekly_hours': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['atados_core']