# -*-coding:utf-8 -*-
__author__ = 'ZZ'
from urllib import urlopen
import re
import time
import random

# pattern to match the id of match
pattern_matchid = re.compile('<td\s+class="td1".*?>(.*?)</td>')
# pattern to match other info of match
pattern_matchinfo = re.compile('<td\s+class="tdC".*?>(.*?)</td>')
# pattern to match the type of match
inner_pattern_matchtype = re.compile('<font.*?>(.*?)</font>')
# pattern to match the name of match
inner_pattern_matchname = re.compile('<a\s+href="(.*?)".*?>(.*?)</a>')
# pattern to match the time of match
inner_pattern_matchtime = re.compile('[\d\-: ]+')
# pattern to pool link
pattern_matchplink = re.compile(u'<a\s+href="(.*?)".*?>固定奖金</a>')

# raw html code from match list. maybe need .decode("gb2312") in server
match_html = urlopen("http://info.sporttery.cn/football/match_list.php").read()

# lists to save data
matchid_lst = []
matchname_lst = []
matchlink_lst = []
matchtype_lst = []
matchtime_lst = []
matchplink_lst = []

# grab match id
for matchid in pattern_matchid.findall(match_html):
    matchid_lst.append(matchid)
# grab match info(include type, vs name, link, time)
for matchinfo in pattern_matchinfo.findall(match_html):
    if len(matchinfo.strip()) > 0:
        matchtype_result = inner_pattern_matchtype.match(matchinfo)
        if (matchtype_result):
            matchtype_lst.append(matchtype_result.group(1))
        matchname_result = inner_pattern_matchname.match(matchinfo)
        if (matchname_result):
            if not matchname_result.group(2).startswith('<'):
                matchlink_lst.append(matchname_result.group(1))
                matchname_lst.append(matchname_result.group(2))
        matchtime_result = inner_pattern_matchtime.match(matchinfo)
        if (matchtime_result):
            matchtime_lst.append(matchtime_result.group(0))

# grab pool link of each match
# for match_link in matchlink_lst:
#     if not match_link.endswith('/'):
#         match_link = match_link + '/'
#     conn = urlopen(match_link)
#     time.sleep(1)
#     match_html = conn.read().decode("gb2312")
#     for i in pattern_matchplink.findall(match_html):
#         print i
#     conn.close()
#     time.sleep(random.randint(5, 9))


# test output
if (False):
    for name in matchlink_lst:
        print name
