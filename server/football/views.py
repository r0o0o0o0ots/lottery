from django.http import HttpResponse
import json
from .models import CurrentMatch

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

