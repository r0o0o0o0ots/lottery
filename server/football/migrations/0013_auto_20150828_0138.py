# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0012_traditionalbill_multiple'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traditionalbill',
            name='content',
            field=models.CharField(max_length=90),
        ),
    ]
