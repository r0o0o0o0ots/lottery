# -*-coding:utf-8-*-
__author__ = 'zz'
from Graber import Graber
from ShowMsg import ShowMsg

class MatchMatches:

    def matchLists(self, html):

        ShowMsg.showMsg("Getting matches infos...")
        # pattern_matchid = re.compile('<td\s+class="td1".*?>(.*?)</td>')
        matchid_lst = Graber.grabAll('<td\s+class="td1".*?>(.*?)</td>', html)
        # pattern_matchtype = re.compile('<td\s+class="tdC".*?><font.*?>(.*?)</font></td>')
        matchtype_lst = Graber.grabAll('<td\s+class="tdC".*?><font.*?>(.*?)</font></td>', html)
        # pattern_matchname = re.compile('<td\s+class="tdC".*?><a\s+href="(.*?)".*?>(.*?VS.*?)</a></td>')
        matchname_lst = Graber.grabAll('<td\s+class="tdC".*?><a\s+href="(.*?)".*?>(.*?VS.*?)</a></td>', html)
        # pattern_matchtime = re.compile('<td\s+class="tdC".*?>([\d\-: ]+)</td>')
        matchtime_lst = Graber.grabAll('<td\s+class="tdC".*?>([\d\-: ]+)</td>', html)

        match_list = []
        index = 0
        for matcher in matchid_lst:
            tmp_dir = dict(id=matcher)
            match_list.append(tmp_dir)
        for matcher in matchtype_lst:
            match_list[index]['type'] = matcher
            index = index + 1
        index = 0
        for item in matchname_lst:
            match_list[index]['link'] = item[0]
            match_list[index]['mid'] = Graber.group('^http.*?m=(\d+)', item[0], 1)
            match_list[index]['name'] = item[1]
            index = index + 1
        index = 0
        for time in matchtime_lst:
            match_list[index]['time'] = time
            index = index + 1
        ShowMsg.showMsgEndline("\tdone.")
        return match_list
