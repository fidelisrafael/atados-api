# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0017_city_highligh'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='highligh',
            new_name='highlight',
        ),
    ]
