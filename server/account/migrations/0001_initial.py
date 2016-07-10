# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_number', models.CharField(unique=True, max_length=11)),
                ('password', models.CharField(max_length=77)),
                ('nick_name', models.CharField(max_length=20)),
                ('real_name', models.CharField(max_length=20)),
                ('sex', models.BooleanField()),
                ('alipay_id', models.CharField(max_length=50)),
                ('balance_unfixed', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
                ('balance_fixed', models.DecimalField(default=0.0, max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='AccountHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.DecimalField(max_digits=10, decimal_places=2)),
                ('type', models.PositiveSmallIntegerField()),
                ('acct', models.ForeignKey(to='account.Account')),
            ],
        ),
    ]
