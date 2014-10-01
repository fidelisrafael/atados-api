# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nonprofit',
            name='owner',
            field=models.ForeignKey(related_name=b'nonprofits', default=8510, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
