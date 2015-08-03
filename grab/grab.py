# -*-coding:utf-8 -*-
__author__ = 'ZZ'
from viewer.HtmlViewer import HtmlViewer
# import re
# import time
# import random
#
# # pattern to match the id of match
# pattern_matchid = re.compile('<td\s+class="td1".*?>(.*?)</td>')
# # pattern to match other info of match
# pattern_matchinfo = re.compile('<td\s+class="tdC".*?>(.*?)</td>')
# # pattern to match the type of match
# inner_pattern_matchtype = re.compile('<font.*?>(.*?)</font>')
# # pattern to match the name of match
# inner_pattern_matchname = re.compile('<a\s+href="(.*?)".*?>(.*?)</a>')
# # pattern to match the time of match
# inner_pattern_matchtime = re.compile('[\d\-: ]+')
# # pattern to pool link
# pattern_matchplink = re.compile(u'<a\s+href="(.*?)".*?>受注赛程</a>')
#
# # raw html code from match list. maybe need .decode("gb2312") in server
# match_html = urlopen("http://info.sporttery.cn/football/match_list.php").read()

hw = HtmlViewer("www.sporttery.cn")
hw.tryConnect()
hw.getHtml()
hw.forward(u"受注赛程")
hw.back()
hw.forward(u"赛果开奖")
hw.back()
hw.forward(u"比分直播")
hw.back()