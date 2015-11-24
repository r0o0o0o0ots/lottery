from django.http import HttpResponse
import json
from account.models import Account
from .models import Match,CurrentMatch
from .models import FootballBill,FootballBillDetail
from .models import TraditionalGame,TraditionalMatches,TraditionalBill
from datetime import datetime
import itertools

def error(msg):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']=msg
    s=json.dumps(data)
    r.write(s)
    return r

def getAcct(params):
    email=params.get('email')
    password=params.get('password')
    accts=Account.objects.filter(email=email,password=password)
    if len(accts)!=1:
        return None
    return accts[0]

def getBill(params,acct):
    billid=params.get('billid')
    bills=FootballBill.objects.filter(acct=acct,id=billid)
    if len(bills)!=1:
        return None
    bill=bills[0]
    return bill

def getTraditionalBill(params,acct):
    billid=params.get('billid')
    bills=TraditionalBill.objects.filter(acct=acct,id=billid)
    if len(bills)!=1:
        return None
    bill=bills[0]
    return bill

def calBetCount(combs,counts):
    bet_count=0
    match_count=len(counts)
    for m in combs:
        if m>match_count:
            return -1
        for comb in itertools.combinations(counts,m):
            count=reduce(lambda x,y:x*y,comb)
            bet_count+=count
    return bet_count

# Create your views here.
def getMatchInfo(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')

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

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['matches']=matches_info
    s=json.dumps(data)
    r.write(s)
    return r

def createBill(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    matchesInfo=params.get('matches')
    combs=params.get('combs')
    multiple=params.get('multiple')

    fb=FootballBill()
    fb.acct=acct
    fb.comb_type=combs
    fb.match_count=len(matchesInfo)
    fb.multiple=multiple
    fb.save()
    selected_options_counts=[]
    for matchInfo in matchesInfo:
        match=Match.objects.get(pk=matchInfo['id'])
        cmatches=CurrentMatch.objects.filter(match=match)
        if len(cmatches)!=1:
            return error('no one current match')
        odd=cmatches[0].odd
        fbd=FootballBillDetail()
        fbd.bill=fb
        fbd.match=match
        fbd.odd=odd
        fbd.content=matchInfo['selectedOptions']
        selected_options_counts.append(len(fbd.content))
        fbd.save()
    bet_count=calBetCount(fb.comb_type,selected_options_counts)
    if bet_count==-1:
        return error('bet count error')
    fb.bet_count=bet_count
    fb.save()

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['billid']=fb.id
    s=json.dumps(data)
    r.write(s)
    return r

def getFootballBills(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]
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
        #fbds=FootballBillDetail.objects.filter(bill=bill)
        #matches=[]
        #for fbd in fbds:
        #    matches.append({'home':fbd.match.home,'away':fbd.match.away,'handicap':fbd.match.handicap,'selectedOptions':fbd.content})
        #billInfo['matches']=matches
        billsInfo.append(billInfo)

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['bills']=billsInfo
    s=json.dumps(data)
    r.write(s)
    return r

def getFootballBillDetail(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=FootballBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('no such bill')
    #    #data['errmsg']='no such bill'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getBill(params,acct)
    if bill==None:
        return error('no such bill')
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

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['bill']=billInfo
    s=json.dumps(data)
    r.write(s)
    return r

def payFootball(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=FootballBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('bill id error')
    #    #data['errmsg']='bill id error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getBill(params,acct)
    if bill==None:
        return error('no such bill')
    if bill.is_payed:
        return error('already payed')
        #data['errmsg']='already payed'
        #s=json.dumps(data)
        #r.write(s)
        #return r

    money=2*bill.bet_count*bill.multiple
    balancef=acct.balance_fixed
    balanceu=acct.balance_unfixed
    if money>balancef+balanceu:
        return error('no enough money')
        #data['errmsg']='no enough money'
        #s=json.dumps(data)
        #r.write(s)
        #return r
    
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

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r

def delFootballBill(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=FootballBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('bill id error')
    #    #data['errmsg']='bill id error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getBill(params,acct)
    if bill==None:
        return error('no such bill')
    if bill.is_payed:
        return error('already payed, can not be deleted')
        #data['errmsg']='already payed, can not be deleted'
        #s=json.dumps(data)
        #r.write(s)
        #return r

    fbds=FootballBillDetail.objects.filter(bill=bill)
    for fbd in fbds:
        fbd.delete()
    bill.delete()

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r

def getTraditionalInfo(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    games=TraditionalGame.objects.order_by('-id')
    if len(games)==0:
        return error('no game')
        #data['errmsg']='no game'
        #s=json.dumps(data)
        #r.write(s)
        #return r

    game=games[0]
    tmatches=TraditionalMatches.objects.filter(game=game).order_by('id')
    matches_info=[]
    for tmatch in tmatches:
        match=tmatch.match
        odd=CurrentMatch.objects.filter(match=match)[0].odd
        info={}
        info['id']=match.id
        info['home']=match.home
        info['away']=match.away
        info['odd']=odd.odd.split(' ')[:3]
        matches_info.append(info)

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['id']=game.id
    data['SN']=game.SN
    data['deadline']=game.deadline.strftime('%Y-%m-%d %H:%M:%S')
    data['matches']=matches_info
    s=json.dumps(data)
    r.write(s)
    return r

def createTraditionalBill(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    id=params.get('id')
    multiple=params.get('multiple')
    type=params.get('type')
    matches=params.get('matches')

    bill=TraditionalBill()
    bill.acct=acct
    bill.type=type
    bill.multiple=multiple
    game=TraditionalGame.objects.get(pk=id)
    bill.game=game
    bill.content=json.dumps(matches)
    comb_type=[int(type)]
    selected_options_counts=map(len,matches)
    bet_count=calBetCount(comb_type,selected_options_counts)
    if bet_count==-1:
        return error('bet count error')
    bill.bet_count=bet_count;
    bill.save()

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['billid']=bill.id
    s=json.dumps(data)
    r.write(s)
    return r

def getTraditionalBills(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]
    bills=TraditionalBill.objects.filter(acct=acct)
    billsInfo=[]
    for bill in bills:
        billInfo={}
        billInfo['id']=bill.id
        #billInfo['time']=bill.time.strftime('%Y-%m-%d %H:%M:%S')
        billInfo['type']=bill.type
        #billInfo['multiple']=bill.multiple
        billInfo['is_payed']=bill.is_payed
        billInfo['bet_count']=bill.bet_count
        #billInfo['bonus']=str(bill.bonus)
        #billInfo['content']=bill.content
        billInfo['finished']=bill.game.results!='x'
        billsInfo.append(billInfo)

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['bills']=billsInfo
    s=json.dumps(data)
    r.write(s)
    return r

def getTraditionalBillDetail(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=TraditionalBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('no such bill')
    #    #data['errmsg']='no such bill'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getTraditionalBill(params,acct)
    if bill==None:
        return error('no such bill')
    billInfo={}
    billInfo['id']=bill.id
    billInfo['time']=bill.time.strftime('%Y-%m-%d %H:%M:%S')
    billInfo['type']=bill.type
    billInfo['multiple']=bill.multiple
    billInfo['is_payed']=bill.is_payed
    billInfo['bet_count']=bill.bet_count
    billInfo['bonus']=str(bill.bonus)
    billInfo['finished']=bill.game.results!='x'
    content=json.loads(bill.content)
    tmatches=TraditionalMatches.objects.filter(game=bill.game).order_by('id')
    matches_info=[]
    for i,tmatch in enumerate(tmatches):
        match=tmatch.match
        match_info={}
        match_info['home']=match.home
        match_info['away']=match.away
        match_info['selectedOptions']=content[i]
        matches_info.append(match_info)
    billInfo['matches']=matches_info

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    data['bill']=billInfo
    s=json.dumps(data)
    r.write(s)
    return r

def delTraditionalBill(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=TraditionalBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('bill id error')
    #    #data['errmsg']='bill id error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getBill(params,acct)
    if bill==None:
        return error('no such bill')
    if bill.is_payed:
        return error('already payed, can not be deleted')
        #data['errmsg']='already payed, can not be deleted'
        #s=json.dumps(data)
        #r.write(s)
        #return r
    bill.delete()

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r

def payTraditionalBill(request):
    params = json.loads(request.body)
    acct=getAcct(params)
    if acct==None:
        return error('user error')
    #email=params.get('email')
    #password=params.get('password')
    #accts=Account.objects.filter(email=email,password=password)
    #if len(accts)!=1:
    #    return error('user error')
    #    #data['errmsg']='user error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r
    #acct=accts[0]

    #billid=params.get('billid')
    #bills=TraditionalBill.objects.filter(acct=acct,id=billid)
    #if len(bills)!=1:
    #    return error('bill id error')
    #    #data['errmsg']='bill id error'
    #    #s=json.dumps(data)
    #    #r.write(s)
    #    #return r

    #bill=bills[0]
    bill=getBill(params,acct)
    if bill==None:
        return error('no such bill')
    if bill.is_payed:
        return error('already payed')
        #data['errmsg']='already payed'
        #s=json.dumps(data)
        #r.write(s)
        #return r
    if bill.game.deadline<datetime.now():
        return error('deadline exceeded')

    money=2*bill.bet_count*bill.multiple
    balancef=acct.balance_fixed
    balanceu=acct.balance_unfixed
    if money>balancef+balanceu:
        return error('no enough money')
        #data['errmsg']='no enough money'
        #s=json.dumps(data)
        #r.write(s)
        #return r
    
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

    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}
    data['errmsg']='success'
    s=json.dumps(data)
    r.write(s)
    return r
