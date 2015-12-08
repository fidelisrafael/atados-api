# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atados_core', '0015_subscription_card_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='cardholder_name',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='cvv',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='exp_month',
        ),
        migrations.RemoveField(
            model_name='subscription',
            name='exp_year',
        ),
    ]
