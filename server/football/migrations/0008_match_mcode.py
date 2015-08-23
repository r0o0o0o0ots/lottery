# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0007_auto_20150821_0320'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='mcode',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
