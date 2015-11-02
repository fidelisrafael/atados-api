# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0006_auto_20150820_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='Name', blank=True)),
                ('email', models.CharField(max_length=200, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=200, verbose_name='Phone', blank=True)),
                ('doc', models.CharField(max_length=200, verbose_name='Doc', blank=True)),
                ('street', models.CharField(max_length=200, verbose_name='Street', blank=True)),
                ('number', models.CharField(max_length=200, verbose_name='Number', blank=True)),
                ('complement', models.CharField(max_length=200, verbose_name='Complement', blank=True)),
                ('city', models.CharField(max_length=200, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=200, verbose_name='State', blank=True)),
                ('value', models.FloatField(default=0.0)),
                ('active', models.BooleanField(default=False)),
                ('recurrent', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('deleted', models.BooleanField(default=False, verbose_name='Deleted')),
                ('deleted_date', models.DateTimeField(null=True, verbose_name='Deleted date', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
