# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0010_auto_20151019_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='parent',
            field=models.ForeignKey(default=b'', to='atados_core.Subscription', null=True),
            preserve_default=True,
        ),
    ]
