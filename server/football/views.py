from django.http import JsonResponse
import json
from account.models import Account
from .models import Match,CurrentMatch
from .models import FootballBill,FootballBillDetail
from .models import TraditionalGame,TraditionalMatches,TraditionalBill
from datetime import datetime
import itertools
from django.contrib.auth.hashers import check_password

def require_acct(func):
    def wrapper(request):
        try:
            params = json.loads(request.body)
            phone_number=params.get('phone_number')
            password=params.get('password')
            acct=Account.objects.get(phone_number=phone_number)
            if check_password(password,acct.password):
                request.acct=acct
                return func(request)
        except:
            pass
        return JsonResponse({'errmsg':'user error'})

    return wrapper

#def getAcct(params):
#    phone_number=params.get('phone_number')
#    password=params.get('password')
#    try:
#        acct=Account.objects.get(phone_number=phone_number)
#        if check_password(password,acct.password):
#            return acct
#    except:
#        return None
#    return None

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
@require_acct
def getMatchInfo(request):
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

    data = {}
    data['errmsg']='success'
    data['matches']=matches_info
    return JsonResponse(data)

@require_acct
def createBill(request):
    params = json.loads(request.body)

    matchesInfo=params.get('matches')
    combs=params.get('combs')
    multiple=params.get('multiple')

    acct=request.acct

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
            return JsonResponse({'errmsg':'no one current match'})
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
        return JsonResponse({'errmsg':'bet count error'})
    fb.bet_count=bet_count
    fb.save()

    data = {}
    data['errmsg']='success'
    data['billid']=fb.id
    return JsonResponse(data)

@require_acct
def getFootballBills(request):
    acct=request.acct
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
        billInfo['status']=bill.status
        #fbds=FootballBillDetail.objects.filter(bill=bill)
        #matches=[]
        #for fbd in fbds:
        #    matches.append({'home':fbd.match.home,'away':fbd.match.away,'handicap':fbd.match.handicap,'selectedOptions':fbd.content})
        #billInfo['matches']=matches
        billsInfo.append(billInfo)

    data = {}
    data['errmsg']='success'
    data['bills']=billsInfo
    return JsonResponse(data)

@require_acct
def getFootballBillDetail(request):
    params = json.loads(request.body)
    acct=request.acct
    bill=getBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
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

    data = {}
    data['errmsg']='success'
    data['bill']=billInfo
    return JsonResponse(data)

@require_acct
def payFootball(request):
    params = json.loads(request.body)
    acct=request.acct

    bill=getBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
    if bill.is_payed:
        return JsonResponse({'errmsg':'already payed'})

    money=2*bill.bet_count*bill.multiple
    balancef=acct.balance_fixed
    balanceu=acct.balance_unfixed
    if money>balancef+balanceu:
        return JsonResponse({'errmsg':'no enough money'})
    
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

    return JsonResponse({'errmsg':'success'})

@require_acct
def delFootballBill(request):
    params = json.loads(request.body)
    acct=request.acct

    bill=getBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
    if bill.is_payed:
        return JsonResponse({'errmsg':'already payed, can not be deleted'})

    fbds=FootballBillDetail.objects.filter(bill=bill)
    for fbd in fbds:
        fbd.delete()
    bill.delete()

    return JsonResponse({'errmsg':'success'})

@require_acct
def getTraditionalInfo(request):
    games=TraditionalGame.objects.order_by('-id')
    if len(games)==0:
        return JsonResponse({'errmsg':'no game'})

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

    data = {}
    data['errmsg']='success'
    data['id']=game.id
    data['SN']=game.SN
    data['deadline']=game.deadline.strftime('%Y-%m-%d %H:%M:%S')
    data['matches']=matches_info
    return JsonResponse(data)

@require_acct
def createTraditionalBill(request):
    params = json.loads(request.body)
    acct=request.acct

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
        return JsonResponse({'errmsg':'bet count error'})
    bill.bet_count=bet_count;
    bill.save()

    data = {}
    data['errmsg']='success'
    data['billid']=bill.id
    return JsonResponse(data)

@require_acct
def getTraditionalBills(request):
    acct=request.acct

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

    data = {}
    data['errmsg']='success'
    data['bills']=billsInfo
    return JsonResponse(data)

@require_acct
def getTraditionalBillDetail(request):
    params = json.loads(request.body)
    acct=request.acct

    bill=getTraditionalBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
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

    data = {}
    data['errmsg']='success'
    data['bill']=billInfo
    return JsonResponse(data)

@require_acct
def delTraditionalBill(request):
    params = json.loads(request.body)
    acct=request.acct

    bill=getBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
    if bill.is_payed:
        return JsonResponse({'errmsg':'already payed, can not be deleted'})
    bill.delete()

    return JsonResponse({'errmsg':'success'})

@require_acct
def payTraditionalBill(request):
    params = json.loads(request.body)
    acct=request.acct

    bill=getBill(params,acct)
    if bill==None:
        return JsonResponse({'errmsg':'no such bill'})
    if bill.is_payed:
        return JsonResponse({'errmsg':'already payed'})
    if bill.game.deadline<datetime.now():
        return JsonResponse({'errmsg':'deadline exceeded'})

    money=2*bill.bet_count*bill.multiple
    balancef=acct.balance_fixed
    balanceu=acct.balance_unfixed
    if money>balancef+balanceu:
        return JsonResponse({'errmsg':'no enough money'})
    
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

    return JsonResponse({'errmsg':'success'})
