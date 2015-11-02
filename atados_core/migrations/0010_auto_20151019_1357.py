# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0009_auto_20151019_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='cardhash',
            field=models.CharField(max_length=500, null=True, verbose_name='Card', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='city',
            field=models.CharField(max_length=200, null=True, verbose_name='City', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='complement',
            field=models.CharField(max_length=200, null=True, verbose_name='Complement', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='doc',
            field=models.CharField(max_length=200, null=True, verbose_name='Doc', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='email',
            field=models.CharField(max_length=200, null=True, verbose_name='Email', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Name', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='number',
            field=models.CharField(max_length=200, null=True, verbose_name='Number', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='phone',
            field=models.CharField(max_length=200, null=True, verbose_name='Phone', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='state',
            field=models.CharField(max_length=200, null=True, verbose_name='State', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='subscription',
            name='street',
            field=models.CharField(max_length=200, null=True, verbose_name='Street', blank=True),
            preserve_default=True,
        ),
    ]
