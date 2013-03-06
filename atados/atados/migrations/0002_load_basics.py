# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from atados.project.models import Availability, Cause
from flatblocks.models import FlatBlock
from atados.project.models import Skill


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

    def backwards(self, orm):
        raise RuntimeError("Cannot reverse this migration.")

    models = {
        'atados.availability': {
            'Meta': {'object_name': 'Availability'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'weekday': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'atados.cause': {
            'Meta': {'object_name': 'Cause'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'atados.skill': {
            'Meta': {'object_name': 'Skill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['atados']
