# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0016_traditionalbill_is_payed'),
    ]

    operations = [
        migrations.AddField(
            model_name='traditionalbill',
            name='bet_count',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
