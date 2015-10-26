# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0013_auto_20151019_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(max_length=500, null=True, verbose_name='Status', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status_reason',
            field=models.CharField(max_length=500, null=True, verbose_name='Status', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='tid',
            field=models.CharField(max_length=500, null=True, verbose_name='Tid', blank=True),
            preserve_default=True,
        ),
    ]
