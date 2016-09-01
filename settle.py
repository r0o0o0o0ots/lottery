import json
import sys,os
import django
from django.db import transaction
import itertools

sys.path.append('./server/')
os.environ['DJANGO_SETTINGS_MODULE']='server.settings'
django.setup()
from football.models import Match,FootballBillDetail,FootballBill

base=2
result_text=['HAD3','HAD1','HAD0','HHAD3','HHAD1','HHAD0',0,1,2,3,4,5,6,7,'33','31','30','13','11','10','03','01','00',
              '1:0','2:0','2:1','3:0','3:1','3:2','4:0','4:1','4:2','5;0','5:1','5:2','other3',
              '0:0','1:1','2:2','3:3','other1',
              '0:1','0:2','1:2','0:3','1:3','2:3','0:4','1:4','2:4','0:5','1:5','2:5','other0'];

def calResults(match):
    result=[]
    result.append(result_text.index('HAD'+match.HAD))
    result.append(result_text.index('HHAD'+match.HHAD))
    TTG=match.TTG
    if TTG>7:
        TTG=7
    result.append(result_text.index(TTG))
    result.append(result_text.index(match.HFT))
    CRS=match.CRS
    if not CRS in result_text:
        CRS='other'+match.HAD
    result.append(result_text.index(CRS))
    return result

def settleBill(bill,bonus):
    bill.bonus+=bonus*bill.multiple
    bill.finished_match_count+=1
    bill.save()
    if bill.finished_match_count==bill.bet_count:
        acct=bill.acct
        acct.balence_unfixed+=bill.bonus
        acct.save()
    
def settleDetail(detail):
    bill=detail.bill
    bill.finished_match_count+=1
    if bill.finished_match_count==bill.match_count:
        bill.status=3
    bill.save()

#matches=Match.objects.filter(status=3)
#for match in matches:
#    results=calResults(match)
#    details=FootballBillDetail.objects.filter(match=match)
#    with transaction.atomic():
#        match.results=results
#        match.status=2
#        match.save()
#        for detail in details:
#            settleDetail(detail)

bills=FootballBill.objects.filter(status=3)
for bill in bills:
    win_odds=[]
    details=FootballBillDetail.objects.filter(bill=bill)
    for detail in details:
        content=json.loads(detail.content)
        results=json.loads(detail.match.results)
        win_results=set(content)&set(results)
        odd=json.loads('['+detail.odd.odd.replace(' ',',')+']')
        win_odd=[odd[i] for i in win_results]
        win_odds.append(win_odd)
    print win_odds
    print 

    total_bonus=0
    comb_type=json.loads(bill.comb_type)
    for comb in comb_type:
        win_odds_comb=itertools.combinations(win_odds,comb)
        for c in win_odds_comb:
            c=list(c)
            print c
            win_odds_prod=itertools.product(*c)
            bonus=1
            for p in win_odds_prod:
                print p
                bonus=reduce(lambda x,y:x*y,p)
                print bonus
                total_bonus+=bonus
    print total_bonus


    #with transaction.atomic():
    #    bill.status=4
    #    bill.save()

#from football.models import CurrentMatch,Odd
#with transaction.atomic():
#    for i in range(5,8):
#        match=Match.objects.get(pk=i)
#        match.status=0
#        match.save()
#        odd=Odd.objects.get(pk=i)
#        cmatch=CurrentMatch()
#        cmatch.match=match
#        cmatch.odd=odd
#        cmatch.save()
