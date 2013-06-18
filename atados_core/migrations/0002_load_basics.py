# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.sites.models import Site
from flatblocks.models import FlatBlock
from atados_core.models import State, City, Suburb, Skill, Availability, Cause

class Migration(DataMigration):

    def forwards(self, orm):
        for slug in ['terms', 'privacy', 'security', 'about']:
            flatblock = FlatBlock()
            flatblock.content = flatblock.slug = slug
            flatblock.save()

        site = Site.objects.get(pk=1)
        site.domain = 'beta.atados.com.br'
        site.name = 'Atados'
        site.save()
        
        for name in ('Capacitação Profissional',
                     'Combate à Pobreza',
                     'Consumo Consciente',
                     'Crianças e Jovens',
                     'Cultura e Esporte',
                     'Defesa de Direitos',
                     'Educação',
                     'Idosos',
                     'Meio Ambiente',
                     'Participação Cidadã',
                     'Proteção Animal',
                     'Saúde',):
            cause = orm.Cause()
            cause.name = name
            cause.save()

        for name in ('Artes/Artesanato',
                     'Comunicação',
                     'Dança/Música',
                     'Direito',
                     'Educação',
                     'Esportes',
                     'Gastronomia',
                     'Gestão',
                     'Idiomas',
                     'Informática/Eletrônicos',
                     'Saúde/Psicologia',
                     'Outros',):
            skill = orm.Skill()
            skill.name = name
            skill.save()


        for weekday in range(7):
            for period in range(3):
                availability = orm.Availability()
                availability.weekday = weekday
                availability.period = period
                availability.save()

        state = orm.State()
        state.name = 'São Paulo'
        state.save()

        city = orm.City()
        city.state = state
        city.name = 'São Paulo'
        city.save()

        for name in ('Zona Leste',
                     'Zona Oeste',
                     'Zona Sul',
                     'Zona Norte',
                     'Centro',):
            suburb = orm.Suburb()
            suburb.city = city
            suburb.name = name
            suburb.save()

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
