# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0007_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='cardhash',
            field=models.CharField(max_length=200, null=True, verbose_name='Card'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='subscription',
            name='parent',
            field=models.ForeignKey(default=False, to='atados_core.Subscription', null=True),
            preserve_default=True,
        ),
    ]
