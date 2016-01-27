# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0020_project_gdd_highlighted'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='month',
            field=models.CharField(max_length=500, null=True, verbose_name='Month payment', blank=True),
            preserve_default=True,
        ),
    ]
