from django.db import models
from account.models import Account

# Create your models here.
class Match(models.Model):
    home=models.CharField(max_length=20)
    away=models.CharField(max_length=20)
    handicap=models.BooleanField()
    odds=models.CharField(max_length=500)
    results=models.CharField(max_length=5)

    def get_odds():
        pass
    def set_odds():
        pass
    def get_results():
        pass
    def set_results():
        pass

class CurrentMatch(models.Model):
    cmatch=models.ForeignKey(Match)

class FootballBill(models.Model):
    acct=models.ForeignKey(Account)
    #type=models.PositiveSmallIntegerField()
    comb_type=models.PositiveSmallIntegerField()
    bet_count=models.PositiveIntegerField()
    match_count=models.PositiveSmallIntegerField()
    finished_match_count=models.PositiveSmallIntegerField(default=0)
    times=models.PositiveSmallIntegerField(default=1)
    is_payed=models.BooleanField(default=0)
    bonus=models.DecimalField(max_digits=10,decimal_places=2,default=0.0)

class FootballBillDetail(models.Model):
    bill=models.ForeignKey(FootballBill)
    match=models.ForeignKey(Match)
    content=models.CharField(max_length=100)

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
