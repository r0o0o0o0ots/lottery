# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0004_auto_20150815_1023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='CRT',
        ),
        migrations.AddField(
            model_name='match',
            name='CRS',
            field=models.CharField(default=b'x:x', max_length=5),
        ),
        migrations.AlterField(
            model_name='match',
            name='HAD',
            field=models.CharField(default=b'x', max_length=1),
        ),
        migrations.AlterField(
            model_name='match',
            name='HFT',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='HHAD',
            field=models.CharField(default=b'x', max_length=1),
        ),
        migrations.AlterField(
            model_name='match',
            name='TTG',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
