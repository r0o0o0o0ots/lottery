# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0013_auto_20150828_0138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traditionalbill',
            name='content',
            field=models.CharField(max_length=115),
        ),
    ]
