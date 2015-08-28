# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0015_traditionalbill_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='traditionalbill',
            name='is_payed',
            field=models.BooleanField(default=False),
        ),
    ]
