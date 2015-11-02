# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0012_auto_20151019_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='status',
            field=models.CharField(default='', max_length=500, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='status_reason',
            field=models.CharField(default='', max_length=500, verbose_name='Status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='tid',
            field=models.CharField(default='', max_length=500, verbose_name='Tid'),
            preserve_default=False,
        ),
    ]
