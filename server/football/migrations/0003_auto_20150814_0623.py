# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0002_auto_20150814_0549'),
    ]

    operations = [
        migrations.RenameField(
            model_name='currentmatch',
            old_name='cmatch',
            new_name='match',
        ),
        migrations.RenameField(
            model_name='currentmatch',
            old_name='codd',
            new_name='odd',
        ),
    ]
