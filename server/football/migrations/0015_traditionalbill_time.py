# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0014_auto_20150828_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='traditionalbill',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 2, 39, 56, 334907, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
