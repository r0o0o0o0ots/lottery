# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentMatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='FootballBill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('comb_type', models.CharField(max_length=7)),
                ('bet_count', models.PositiveIntegerField()),
                ('match_count', models.PositiveSmallIntegerField()),
                ('finished_match_count', models.PositiveSmallIntegerField(default=0)),
                ('multiple', models.PositiveSmallIntegerField(default=1)),
                ('is_payed', models.BooleanField(default=0)),
                ('bonus', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('acct', models.ForeignKey(to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='FootballBillDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=54)),
                ('bill', models.ForeignKey(to='football.FootballBill')),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('home', models.CharField(max_length=50)),
                ('away', models.CharField(max_length=50)),
                ('handicap', models.SmallIntegerField()),
                ('HAD', models.CharField(max_length=1)),
                ('HHAD', models.CharField(max_length=1)),
                ('CRT', models.CharField(max_length=5)),
                ('TTG', models.PositiveSmallIntegerField()),
                ('HFT', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Matches14Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Matches14Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matches', models.CharField(max_length=200)),
                ('results', models.CharField(max_length=14)),
            ],
        ),
        migrations.CreateModel(
            name='Matches9Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=60)),
                ('game', models.ForeignKey(to='football.Matches14Game')),
            ],
        ),
        migrations.CreateModel(
            name='Odds',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('odds', models.CharField(max_length=500)),
                ('match', models.ForeignKey(to='football.Match')),
            ],
        ),
        migrations.AddField(
            model_name='matches14bill',
            name='game',
            field=models.ForeignKey(to='football.Matches14Game'),
        ),
        migrations.AddField(
            model_name='footballbilldetail',
            name='match',
            field=models.ForeignKey(to='football.Match'),
        ),
        migrations.AddField(
            model_name='currentmatch',
            name='cmatch',
            field=models.ForeignKey(to='football.Match'),
        ),
        migrations.AddField(
            model_name='currentmatch',
            name='codd',
            field=models.ForeignKey(to='football.Odds'),
        ),
    ]
