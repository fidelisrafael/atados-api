# -*- coding: utf-8 -*-
import datetime
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
        ))
        db.send_create_signal(u'atados_core', ['City'])

        # Adding model 'Suburb'
        db.create_table(u'atados_core_suburb', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.City'])),
        ))
        db.send_create_signal(u'atados_core', ['Suburb'])

        # Adding model 'Address'
        db.create_table(u'atados_core_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('addressline', self.gf('django.db.models.fields.CharField')(default=None, max_length=200, null=True, blank=True)),
            ('addressnumber', self.gf('django.db.models.fields.CharField')(default=None, max_length=10, null=True, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.State'], null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.City'], null=True, blank=True)),
            ('suburb', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['atados_core.Suburb'], null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Address'])

        # Adding model 'Nonprofit'
        db.create_table(u'atados_core_nonprofit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('details', self.gf('django.db.models.fields.TextField')(default=None, max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(default=None, max_length=100, null=True, blank=True)),
            ('cover', self.gf('sorl.thumbnail.fields.ImageField')(default=None, max_length=100, null=True, blank=True)),
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

        # Adding model 'Volunteer'
        db.create_table(u'atados_core_volunteer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(default=None, max_length=100, null=True, blank=True)),
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

        # Adding model 'Project'
        db.create_table(u'atados_core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('nonprofit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Nonprofit'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('details', self.gf('django.db.models.fields.TextField')(max_length=1024)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=75, null=True, blank=True)),
            ('responsible', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(default=None, max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Project'])

        # Adding M2M table for field causes on 'Project'
        m2m_table_name = db.shorten_name(u'atados_core_project_causes')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'atados_core.project'], null=False)),
            ('cause', models.ForeignKey(orm[u'atados_core.cause'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'cause_id'])

        # Adding model 'Donation'
        db.create_table(u'atados_core_donation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Project'], unique=True)),
            ('delivery', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True)),
            ('collection_by_nonprofit', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'atados_core', ['Donation'])

        # Adding model 'Work'
        db.create_table(u'atados_core_work', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Project'], unique=True)),
            ('address', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['atados_core.Address'], unique=True)),
            ('weekly_hours', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('can_be_done_remotely', self.gf('django.db.models.fields.BooleanField')(default=False)),
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

        # Adding M2M table for field skills on 'Work'
        m2m_table_name = db.shorten_name(u'atados_core_work_skills')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('work', models.ForeignKey(orm[u'atados_core.work'], null=False)),
            ('skill', models.ForeignKey(orm[u'atados_core.skill'], null=False))
        ))
        db.create_unique(m2m_table_name, ['work_id', 'skill_id'])

        # Adding model 'Material'
        db.create_table(u'atados_core_material', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('donation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Donation'])),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Material'])

        # Adding model 'Role'
        db.create_table(u'atados_core_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('work', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Work'])),
            ('name', self.gf('django.db.models.fields.CharField')(default=None, max_length=50, null=True, blank=True)),
            ('prerequisites', self.gf('django.db.models.fields.TextField')(default=None, max_length=1024, null=True, blank=True)),
            ('vacancies', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'atados_core', ['Role'])

        # Adding model 'Apply'
        db.create_table(u'atados_core_apply', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('volunteer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Volunteer'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['atados_core.Project'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
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

        # Deleting model 'Suburb'
        db.delete_table(u'atados_core_suburb')

        # Deleting model 'Address'
        db.delete_table(u'atados_core_address')

        # Deleting model 'Nonprofit'
        db.delete_table(u'atados_core_nonprofit')

        # Removing M2M table for field causes on 'Nonprofit'
        db.delete_table(db.shorten_name(u'atados_core_nonprofit_causes'))

        # Deleting model 'Volunteer'
        db.delete_table(u'atados_core_volunteer')

        # Removing M2M table for field causes on 'Volunteer'
        db.delete_table(db.shorten_name(u'atados_core_volunteer_causes'))

        # Removing M2M table for field skills on 'Volunteer'
        db.delete_table(db.shorten_name(u'atados_core_volunteer_skills'))

        # Deleting model 'Project'
        db.delete_table(u'atados_core_project')

        # Removing M2M table for field causes on 'Project'
        db.delete_table(db.shorten_name(u'atados_core_project_causes'))

        # Deleting model 'Donation'
        db.delete_table(u'atados_core_donation')

        # Deleting model 'Work'
        db.delete_table(u'atados_core_work')

        # Removing M2M table for field availabilities on 'Work'
        db.delete_table(db.shorten_name(u'atados_core_work_availabilities'))

        # Removing M2M table for field skills on 'Work'
        db.delete_table(db.shorten_name(u'atados_core_work_skills'))

        # Deleting model 'Material'
        db.delete_table(u'atados_core_material')

        # Deleting model 'Role'
        db.delete_table(u'atados_core_role')

        # Deleting model 'Apply'
        db.delete_table(u'atados_core_apply')

        # Deleting model 'Recommendation'
        db.delete_table(u'atados_core_recommendation')


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
        u'atados_core.apply': {
            'Meta': {'object_name': 'Apply'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['atados_core.Project']"}),
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
            'cover': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'atados_core.project': {
            'Meta': {'object_name': 'Project'},
            'causes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['atados_core.Cause']", 'symmetrical': 'False'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '1024'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'prerequisites': ('django.db.models.fields.TextField', [], {'default': 'None', 'max_length': '1024', 'null': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
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