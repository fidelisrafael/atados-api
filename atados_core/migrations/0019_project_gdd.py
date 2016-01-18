# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0018_auto_20151221_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gdd',
            field=models.BooleanField(default=False, verbose_name='Dia das boas acoes'),
            preserve_default=True,
        ),
    ]
