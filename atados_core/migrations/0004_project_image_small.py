# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_resized.forms
import atados_core.models


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0003_auto_20141003_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image_small',
            field=django_resized.forms.ResizedImageField(default=None, null=True, upload_to=atados_core.models.project_image_name_small, blank=True),
            preserve_default=True,
        ),
    ]
