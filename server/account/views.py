from django.shortcuts import render
from django.http import HttpResponse
from .models import Account
import json

# Create your views here.
def get_detail(request):
    email = request.GET['email']
    accounts = Account.objects.filter(email=email)
    if len(accounts)!=1:
        return HttpResponse("error")
    account = accounts[0]
    detail = {}
    detail['nick_name'] = account.nick_name
    detail['real_name'] = account.real_name
    detail['sex'] = account.sex
    detail['email'] = account.email
    detail['phone_number'] = account.phone_number
    detail['alipay_id'] = account.alipay_id
    detail['balance_unfixed'] = str(account.balance_unfixed)
    detail['balance_fixed']= str(account.balance_fixed)

    s = json.dumps(detail)
    return HttpResponse(s)
