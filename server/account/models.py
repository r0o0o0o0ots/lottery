from django.db import models

# Create your models here.
account_history_types=['charge','buy','bonus','draw','give','accept']

class Account(models.Model):
    phone_number=models.CharField(max_length=11,unique=True)
    password=models.CharField(max_length=77)
    nick_name=models.CharField(max_length=20)
    real_name=models.CharField(max_length=20)
    sex=models.BooleanField()
    alipay_id=models.CharField(max_length=50)
    balance_unfixed=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    balance_fixed=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

class AccountHistory(models.Model):
    acct=models.ForeignKey(Account)
    money=models.DecimalField(max_digits=10,decimal_places=2)
    type=models.PositiveSmallIntegerField()
