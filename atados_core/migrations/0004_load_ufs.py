# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."

        saopaulo = orm.State.objects.get(name='São Paulo')
        saopaulo.code = 'SP'
        saopaulo.save()

        parana = orm.State.objects.get(name='Paraná')
        parana.code = 'PR'
        parana.save()

        states = [ ('AC', u'Acre'),
                   ('AL', u'Alagoas'),
                   ('AP', u'Amapá'),
                   ('AM', u'Amazonas'),
                   ('BA', u'Bahia'),
                   ('CE', u'Ceará'),
                   ('DF', u'Distrito Federal'),
                   ('ES', u'Espírito Santo'),
                   ('GO', u'Goiás'),
                   ('MA', u'Maranhão'),
                   ('MT', u'Mato Grosso'),
                   ('MS', u'Mato Grosso do Sul'),
                   ('MG', u'Minas Gerais'),
                   ('PA', u'Pará'),
                   ('PB', u'Paraíba'),
                   #('PR', u'Paraná'),
                   ('PE', u'Pernambuco'),
                   ('PI', u'Piauí'),
                   ('RJ', u'Rio de Janeiro'),
                   ('RN', u'Rio Grande do Norte'),
                   ('RS', u'Rio Grande do Sul'),
                   ('RO', u'Rondônia'),
                   ('RR', u'Roraima'),
                   ('SC', u'Santa Catarina'),
                   #('SP', u'São Paulo'),
                   ('SE', u'Sergipe'),
                   ('TO', u'Tocantins')]

        for item in states:
            state = orm.State()
            state.name = item[1]
            state.code = item[0]
            state.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

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
        }
    }

    complete_apps = ['atados_core']
    symmetrical = True
