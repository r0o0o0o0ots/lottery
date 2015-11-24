# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0019_auto_20151124_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballbill',
            name='bet_count',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
