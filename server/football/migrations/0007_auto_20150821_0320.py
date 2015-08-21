# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0006_auto_20150815_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballbill',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
