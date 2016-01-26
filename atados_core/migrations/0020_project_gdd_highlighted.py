# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0019_project_gdd'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gdd_highlighted',
            field=models.BooleanField(default=False, verbose_name='DBA Highlighted'),
            preserve_default=True,
        ),
    ]
