# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0008_auto_20151019_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='cardhash',
            field=models.CharField(max_length=500, null=True, verbose_name='Card'),
            preserve_default=True,
        ),
    ]
