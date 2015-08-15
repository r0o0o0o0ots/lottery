# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0005_auto_20150815_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='handicap',
            field=models.CharField(max_length=3),
        ),
    ]
