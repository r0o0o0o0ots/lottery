from django.db import models

# Create your models here.
account_history_types=['charge','buy','bonus','draw','give','accept']

class Account(models.Model):
    password=models.CharField(max_length=30)
    nick_name=models.CharField(max_length=30)
    real_name=models.CharField(max_length=20)
    sex=models.BooleanField()
    email=models.EmailField(unique=True)
    phone_number=models.CharField(max_length=20)
    alipay_id=models.CharField(max_length=50)
    balance_unfixed=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
    balance_fixed=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

class AccountHistory(models.Model):
    acct=models.ForeignKey(Account)
    money=models.DecimalField(max_digits=10,decimal_places=2)
    type=models.PositiveSmallIntegerField()
