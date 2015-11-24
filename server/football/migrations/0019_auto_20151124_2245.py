# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0018_footballbilldetail_odd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footballbill',
            name='comb_type',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
