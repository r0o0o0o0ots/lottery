from django.http import HttpResponse
from .models import Account
import json

# Create your views here.
def signin(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    # if request.method=='OPTIONS':
    #    r['Access-Control-Allow-Methods']= 'GET,PUT,POST'
    #    r['Access-Control-Allow-Headers']= 'accept, content-type'
    #    r['Access-Control-Max-Age'] = 1728000
    #    return r

    params = json.loads(request.body)
    email = params.get('email')
    password = params.get('password')
    if not email or not password:
        data['errmsg'] = 'Wrong parameters'
        s = json.dumps(data)
        r.write(s)
        return r

    accts = Account.objects.filter(email=email)
    if len(accts) != 1:
        data['errmsg'] = 'No such user'
        s = json.dumps(data)
        r.write(s)
        return r
    acct = accts[0]
    if acct.password != password:
        data['errmsg'] = 'Wrong password'
        s = json.dumps(data)
        r.write(s)
        return r

    data['errmsg'] = 'success'
    data['email'] = acct.email
    data['password']=acct.password
    data['nick_name'] = acct.nick_name
    data['real_name'] = acct.real_name
    data['sex'] = acct.sex
    data['phone_number'] = acct.phone_number
    data['alipay_id'] = acct.alipay_id
    data['balance_unfixed'] = str(acct.balance_unfixed)
    data['balance_fixed'] = str(acct.balance_fixed)
    s = json.dumps(data)
    r.write(s)
    return r


def signup(request):
    r = HttpResponse()
    r['Access-Control-Allow-Origin'] = '*'
    data = {}

    params = json.loads(request.body)
    email = params.get('email')
    password = params.get('password')
    confirm = params.get('confirm')
    nick_name = params.get('nick_name')
    real_name = params.get('real_name')
    sex = params.get('sex')
    phone_number = params.get('phone_number')
    alipay_id = params.get('alipay_id')

    accts = Account.objects.filter(email=email)
    if len(accts) != 0:
        data['errmsg'] = 'Email already used'
        s = json.dumps(data)
        r.write(s)
        return r
    if password != confirm:
        data['errmsg'] = 'Confirm not match'
        s = json.dumps(data)
        r.write(s)
        return r

    acct = Account()
    acct.email = email
    acct.password = password
    acct.nick_name = nick_name
    acct.real_name = real_name
    acct.sex = int(sex)
    acct.phone_number = phone_number
    acct.alipay_id = alipay_id
    acct.save()

    data['errmsg'] = 'success'
    data['email'] = acct.email
    data['password']=acct.password
    data['nick_name'] = acct.nick_name
    data['real_name'] = acct.real_name
    data['sex'] = acct.sex
    data['phone_number'] = acct.phone_number
    data['alipay_id'] = acct.alipay_id
    data['balance_unfixed'] = str(acct.balance_unfixed)
    data['balance_fixed'] = str(acct.balance_fixed)
    s = json.dumps(data)
    r.write(s)
    return r
