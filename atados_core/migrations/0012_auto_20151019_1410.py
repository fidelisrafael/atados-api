# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0011_auto_20151019_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='cardholder_name',
            field=models.CharField(default=0, max_length=200, verbose_name='CardholderName'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='cvv',
            field=models.CharField(default=0, max_length=500, verbose_name='Cvv'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='exp_month',
            field=models.CharField(default=0, max_length=200, verbose_name='ExpMonth'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='exp_year',
            field=models.CharField(default=0, max_length=200, verbose_name='ExpYear'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='cardhash',
            field=models.CharField(default=0, max_length=500, verbose_name='Card'),
            preserve_default=False,
        ),
    ]
