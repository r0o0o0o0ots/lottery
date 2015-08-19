# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('odd', models.CharField(max_length=500)),
                ('match', models.ForeignKey(to='football.Match')),
            ],
        ),
        migrations.RemoveField(
            model_name='odds',
            name='match',
        ),
        migrations.AlterField(
            model_name='currentmatch',
            name='codd',
            field=models.ForeignKey(to='football.Odd'),
        ),
        migrations.DeleteModel(
            name='Odds',
        ),
    ]
