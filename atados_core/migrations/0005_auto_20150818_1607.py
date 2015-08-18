# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import atados_core.models


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0004_project_image_small'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image_large',
            field=django_resized.forms.ResizedImageField(default=None, null=True, upload_to=atados_core.models.project_image_name_large, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='image_medium',
            field=django_resized.forms.ResizedImageField(default=None, null=True, upload_to=atados_core.models.project_image_name_medium, blank=True),
            preserve_default=True,
        ),
    ]
