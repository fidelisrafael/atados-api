# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonprofit',
            name='details',
            field=models.TextField(default=None, max_length=2048, null=True, verbose_name='Details', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='details',
            field=models.TextField(max_length=2048, verbose_name='Details'),
        ),
    ]
