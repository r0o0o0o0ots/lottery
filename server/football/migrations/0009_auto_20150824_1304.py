# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0008_match_mcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='SN',
            field=models.CharField(default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='event',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='match',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 24, 13, 4, 38, 853125, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
