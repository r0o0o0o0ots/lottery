# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '__first__'),
        ('football', '0010_auto_20150824_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='TraditionalBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=5)),
                ('content', models.CharField(max_length=60)),
                ('bonus', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('acct', models.ForeignKey(to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='TraditionalGame',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('SN', models.CharField(max_length=10)),
                ('deadline', models.DateTimeField()),
                ('results', models.CharField(default=b'x', max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='TraditionalMatches',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game', models.ForeignKey(to='football.TraditionalGame')),
                ('match', models.ForeignKey(to='football.Match')),
            ],
        ),
        migrations.RemoveField(
            model_name='matches14bill',
            name='game',
        ),
        migrations.RemoveField(
            model_name='matches9bill',
            name='game',
        ),
        migrations.AlterField(
            model_name='footballbilldetail',
            name='content',
            field=models.CharField(max_length=200),
        ),
        migrations.DeleteModel(
            name='Matches14Bill',
        ),
        migrations.DeleteModel(
            name='Matches14Game',
        ),
        migrations.DeleteModel(
            name='Matches9Bill',
        ),
        migrations.AddField(
            model_name='traditionalbill',
            name='game',
            field=models.ForeignKey(to='football.TraditionalGame'),
        ),
    ]
