# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0011_auto_20150827_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='traditionalbill',
            name='multiple',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
