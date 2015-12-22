# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0016_auto_20151208_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='highligh',
            field=models.BooleanField(default=False, verbose_name='Highlight this city when listing cities'),
            preserve_default=True,
        ),
    ]
