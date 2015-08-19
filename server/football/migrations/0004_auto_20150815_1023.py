# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0003_auto_20150814_0623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='odd',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
