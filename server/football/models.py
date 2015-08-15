from django.db import models
from account.models import Account

# Create your models here.
class Match(models.Model):
    home=models.CharField(max_length=50)
    away=models.CharField(max_length=50)
    handicap=models.SmallIntegerField()
    HAD=models.CharField(max_length=1,default='x')
    HHAD=models.CharField(max_length=1,default='x')
    CRS=models.CharField(max_length=5,default='x:x')
    TTG=models.PositiveSmallIntegerField(default=0)
    HFT=models.PositiveSmallIntegerField(default=0)

class Odd(models.Model):
    match=models.ForeignKey(Match)
    time=models.DateTimeField(auto_now=True)
    odd=models.CharField(max_length=500)

class CurrentMatch(models.Model):
    match=models.ForeignKey(Match)
    odd=models.ForeignKey(Odd)

class FootballBill(models.Model):
    acct=models.ForeignKey(Account)
    time=models.DateTimeField()
    #type=models.PositiveSmallIntegerField()
    comb_type=models.CharField(max_length=7)
    bet_count=models.PositiveIntegerField()
    match_count=models.PositiveSmallIntegerField()
    finished_match_count=models.PositiveSmallIntegerField(default=0)
    multiple=models.PositiveSmallIntegerField(default=1)
    is_payed=models.BooleanField(default=0)
    bonus=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

class FootballBillDetail(models.Model):
    bill=models.ForeignKey(FootballBill)
    match=models.ForeignKey(Match)
    content=models.CharField(max_length=54)

#class FootballBet(models.Model):
#    bill=models.ForeignKey(FootballBill)
#    type=models.PositiveSmallIntegerField()
#    won=models.NullBooleanField()
#    bonus=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)
#
#class FootballBetDetail(models.Model):
#    bet=models.ForeignKey(FootballBet)
#    match=models.ForeignKey(Match)
#    content=models.PositiveSmallIntegerField()

class Matches14Game(models.Model):
    matches=models.CharField(max_length=200)
    results=models.CharField(max_length=14)

class Matches14Bill(models.Model):
    game=models.ForeignKey(Matches14Game)
    content=models.CharField(max_length=60)

class Matches9Bill(models.Model):
    game=models.ForeignKey(Matches14Game)
    content=models.CharField(max_length=60)
