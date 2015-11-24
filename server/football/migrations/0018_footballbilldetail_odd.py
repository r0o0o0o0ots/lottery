# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0017_traditionalbill_bet_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballbilldetail',
            name='odd',
            field=models.ForeignKey(default=1, to='football.Odd'),
            preserve_default=False,
        ),
    ]
