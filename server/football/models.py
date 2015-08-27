from django.db import models
from account.models import Account

# Create your models here.
class Match(models.Model):
    home=models.CharField(max_length=50)
    away=models.CharField(max_length=50)
    SN=models.CharField(max_length=10)
    event=models.CharField(max_length=20)
    time=models.DateTimeField()
    handicap=models.CharField(max_length=3)
    HAD=models.CharField(max_length=1,default='x')
    HHAD=models.CharField(max_length=1,default='x')
    CRS=models.CharField(max_length=5,default='x:x')
    TTG=models.PositiveSmallIntegerField(default=0)
    HFT=models.PositiveSmallIntegerField(default=0)
    mcode=models.CharField(max_length=10)

class Odd(models.Model):
    match=models.ForeignKey(Match)
    time=models.DateTimeField(auto_now=True)
    odd=models.CharField(max_length=500)

class CurrentMatch(models.Model):
    match=models.ForeignKey(Match)
    odd=models.ForeignKey(Odd)

class FootballBill(models.Model):
    acct=models.ForeignKey(Account)
    time=models.DateTimeField(auto_now=True)
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
    content=models.CharField(max_length=200)

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

class TraditionalGame(models.Model):
    SN=models.CharField(max_length=10)
    deadline=models.DateTimeField()
    results=models.CharField(max_length=14,default='x')

class TraditionalMatches(models.Model):
    game=models.ForeignKey(TraditionalGame)
    match=models.ForeignKey(Match)

class TraditionalBill(models.Model):
    acct=models.ForeignKey(Account)
    type=models.CharField(max_length=5)
    multiple=models.PositiveSmallIntegerField(default=1)
    game=models.ForeignKey(TraditionalGame)
    content=models.CharField(max_length=60)
    bonus=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

#class Matches9Bill(models.Model):
#    game=models.ForeignKey(Matches14Game)
#    content=models.CharField(max_length=60)
