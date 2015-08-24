# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0009_auto_20150824_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='mcode',
            field=models.CharField(max_length=10),
        ),
    ]
