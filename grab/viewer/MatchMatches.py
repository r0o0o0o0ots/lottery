# -*-coding:utf-8-*-
__author__ = 'zz'
import re
from ShowMsg import ShowMsg

class MatchMatches:

    def matchLists(self, html):

        ShowMsg.showMsgEndline("Getting matches infos...")
        pattern_matchid = re.compile('<td\s+class="td1".*?>(.*?)</td>')
        pattern_matchtype = re.compile('<td\s+class="tdC".*?><font.*?>(.*?)</font></td>')
        pattern_matchname = re.compile('<td\s+class="tdC".*?><a\s+href="(.*?)".*?>(.*?VS.*?)</a></td>')
        pattern_matchtime = re.compile('<td\s+class="tdC".*?>([\d\-: ]+)</td>')

        match_list = []
        index = 0
        for matcher in pattern_matchid.findall(html):
            tmp_list = []
            tmp_list.append(matcher)
            match_list.append(tmp_list)
        for matcher in pattern_matchtype.findall(html):
            match_list[index].append(matcher)
            index = index + 1
        index = 0
        for link, name in pattern_matchname.findall(html):
            match_list[index].append(link)
            match_list[index].append(name)
            index = index + 1
        index = 0
        for time in pattern_matchtime.findall(html):
            match_list[index].append(time)
            index = index + 1

        # for test
        for m in match_list:
            ShowMsg.showMsgEndline(','.join(m))
