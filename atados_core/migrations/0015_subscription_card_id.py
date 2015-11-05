# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0014_auto_20151029_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='card_id',
            field=models.CharField(default=0, max_length=500, verbose_name='Card ID'),
            preserve_default=False,
        ),
    ]
