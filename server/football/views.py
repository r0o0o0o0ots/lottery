from django.http import HttpResponse
import json
from account.models import Account
from .models import Match,Odd,CurrentMatch
from .models import FootballBill,FootballBillDetail
import math

def calBetCount(combs,n):
    bet_count=0
    for m in combs:
        bet_count+=math.factorial(n)/math.factorial(m)/math.factorial(n-m)
    return bet_count

# Create your views here.
def getMatchInfo(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    matches_info=[]
    cmatches=CurrentMatch.objects.all()
    for cmatch in cmatches:
        match=cmatch.match
        odd=cmatch.odd
        info={}
        info['id']=match.id
        info['home']=match.home
        info['away']=match.away
        info['handicap']=match.handicap
        info['odd']=odd.odd.split(' ')
        matches_info.append(info)

    data['errmsg']='success'
    data['matches']=matches_info
    s=json.dumps(data)
    r.write(s)
    return r

def createBill(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    params = json.loads(request.body)
    email=params.get('email')
    password=params.get('password')
    accts=Account.objects.filter(email=email,password=password)
    if len(accts)!=1:
        data['errmsg']='user error'
        s=json.dumps(data)
        r.write(s)
        return r
    acct=accts[0]
    matchesInfo=params.get('matches')
    combs=params.get('combs')
    multiple=params.get('multiple')

    fb=FootballBill()
    fb.acct=acct
    fb.comb_type=combs
    fb.match_count=len(matchesInfo)
    fb.multiple=multiple
    fb.bet_count=calBetCount(fb.comb_type,fb.match_count)
    fb.save()
    for matchInfo in matchesInfo:
        match=Match.objects.get(pk=matchInfo['id'])
        fbd=FootballBillDetail()
        fbd.bill=fb
        fbd.match=match
        fbd.content=matchInfo['selectedOptions']
        fbd.save()

    data['errmsg']='success'
    data['billid']=fb.id
    s=json.dumps(data)
    r.write(s)
    return r

def getFootballBills(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    params = json.loads(request.body)
    email=params.get('email')
    password=params.get('password')
    accts=Account.objects.filter(email=email,password=password)
    if len(accts)!=1:
        data['errmsg']='user error'
        s=json.dumps(data)
        r.write(s)
        return r
    acct=accts[0]
    bills=FootballBill.objects.filter(acct=acct)
    billsInfo=[]
    for bill in bills:
        billInfo={}
        billInfo['id']=bill.id
        billInfo['time']=bill.time.strftime('%Y-%m-%d %H:%M:%S')
        billInfo['comb_type']=bill.comb_type
        billInfo['bet_count']=bill.bet_count
        billInfo['match_count']=bill.match_count
        billInfo['finished_match_count']=bill.finished_match_count
        billInfo['multiple']=bill.multiple
        billInfo['is_payed']=bill.is_payed
        billInfo['bonus']=str(bill.bonus)
        fbds=FootballBillDetail.objects.filter(bill=bill)
        matches=[]
        for fbd in fbds:
            matches.append({'home':fbd.match.home,'away':fbd.match.away,'handicap':fbd.match.handicap,'selectedOptions':fbd.content})
        billInfo['matches']=matches
        billsInfo.append(billInfo)

    data['errmsg']='success'
    data['bills']=billsInfo
    s=json.dumps(data)
    r.write(s)
    return r

def payFootball(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    params = json.loads(request.body)
    email=params.get('email')
    password=params.get('password')
    billid=params.get('billid')
    accts=Account.objects.filter(email=email,password=password)
    if len(accts)!=1:
        data['errmsg']='user error'
        s=json.dumps(data)
        r.write(s)
        return r
    acct=accts[0]
    bills=FootballBill.objects.filter(acct=acct,id=billid)
    if len(bills)!=1:
        data['errmsg']='bill id error'
        s=json.dumps(data)
        r.write(s)
        return r

    bill=bills[0]
    if bill.is_payed:
        data['errmsg']='already payed'
        s=json.dumps(data)
        r.write(s)
        return r

    money=2*bill.bet_count*bill.multiple
    balancef=acct.balance_fixed
    balanceu=acct.balance_unfixed
    if money>balancef+balanceu:
        data['errmsg']='no enough money'
        s=json.dumps(data)
        r.write(s)
        return r
    
    if balancef>=money:
        balancef=balancef-money
    else:
        balanceu-=money-balancef
        balancef=0
    acct.balance_fixed=balancef
    acct.balance_unfixed=balanceu
    acct.save()
    bill.is_payed=True
    bill.save()

    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r

def delFootballBill(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    params = json.loads(request.body)
    email=params.get('email')
    password=params.get('password')
    billid=params.get('billid')
    accts=Account.objects.filter(email=email,password=password)
    if len(accts)!=1:
        data['errmsg']='user error'
        s=json.dumps(data)
        r.write(s)
        return r
    acct=accts[0]
    bills=FootballBill.objects.filter(acct=acct,id=billid)
    if len(bills)!=1:
        data['errmsg']='bill id error'
        s=json.dumps(data)
        r.write(s)
        return r

    bill=bills[0]
    if bill.is_payed:
        data['errmsg']='already payed, can not be deleted'
        s=json.dumps(data)
        r.write(s)
        return r

    fbds=FootballBillDetail.objects.filter(bill=bill)
    for fbd in fbds:
        fbd.delete()
    bill.delete()

    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r
