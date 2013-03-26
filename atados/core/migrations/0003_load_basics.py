# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from flatblocks.models import FlatBlock
from atados.core.models import State, City, Suburb, Skill, Availability, Cause


class Migration(DataMigration):

    def forwards(self, orm):
        for slug in {'terms', 'privacy', 'security', 'about'}:
            flatblock = FlatBlock()
            flatblock.content = flatblock.slug = slug
            flatblock.save()

        for weekday in range(7):
            for period in range(3):
                availability = Availability()
                availability.weekday = weekday
                availability.period = period
                availability.save()

        for name in {'Artes e Artesanato', 'Comunicação e Marketing',
                     'Contrução e Reparos', 'Educação', 'Esporte',
                     'Gastronomia', 'Gestão', 'Informática e Eletrônicos',
                     'Idiomas', 'Música e Dança', 'Outra'}:
            skill = Skill()
            skill.name = name
            skill.save()

        for name in {'Animal', 'Profissionalização', 'Saúde',
                     'Cultura', 'Meio ambiente', 'Direitos humanos',
                     'Religião'}:
            cause = Cause()
            cause.name = name
            cause.save()

        for id, name in enumerate(['Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
                     'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão',
                     'Mato Grosso', 'Mato Groso do Sul', 'Minas Gerais',
                     'Pará', 'Paraíba', 'Paraná', 'Pernambuco', 'Piauí',
                     'Rio de Janeiro', 'Rio Grande do Norte',
                     'Rio Grande do Sul', 'Rondônia', 'Roraima',
                     'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins']):
            state = State()
            state.id = id + 1
            state.name = name
            state.save()

        sao_paulo = City()
        sao_paulo.name = 'São Paulo'
        sao_paulo.state_id = 25
        sao_paulo.save()

        for name, state_id in {'Guarulhos': 25,
                               'Rio de Janeiro': 19, 'Curitiba': 16}.iteritems():
            city = City()
            city.name = name
            city.state_id = state_id
            city.save()

        for name, city_id in {'Zona Norte': 1, 'Zona Sul': 1,
                              'Zona Leste': 1, 'Zona Oeste': 1,
                              'Centro': 1}.iteritems():
            suburb = Suburb()
            suburb.name = name
            suburb.city_id = city_id
            suburb.save()

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'core.availability': {
            'Meta': {'object_name': 'Availability'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
        }
    }

    complete_apps = ['core']
    symmetrical = True
