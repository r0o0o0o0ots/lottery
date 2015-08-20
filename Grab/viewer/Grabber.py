# -*-coding:utf-8-*-
__author__ = 'zz'
from HtmlViewer import HtmlViewer
from ShowMsg import *
from BeautifulSoup import BeautifulSoup
import codecs
import re

class Grabber:

    def __init__(self, thehomepage):
        self.home_page = thehomepage
        self.viewer = HtmlViewer(self.home_page)
        self.viewer.tryConnect()
        self.viewer.getHtml()

    def analyse(self, info_type='match_list'):

        if info_type == 'match_list':
            self.__getMatches()
        else:
            ShowMsg.showMsgEndline("Undefined analyse contents: "+info_type)


    def __getMatches(self):
        self.viewer.forward(u"受注赛程")
        self.viewer.getHtml()
        soup = BeautifulSoup(self.viewer.html)
        matches_lst = []
        mtable = soup.find(name="table", id="jumpTable")
        mtrs = mtable.findAll(name="tr")
        for tr in mtrs:
            mtds = tr.findAll(name="td")
            if len(mtds) == 12 and u"已开售" in mtds[5]:
                # 0:match_id; 1:match_type; 2:match_team; 3:match_time; 5:if_sale
                match_title = ['mid', 'mtype', 'mm', 'mhref', 'mhometeam', 'mawayteam', 'mtime']
                match_content = []
                match_content.append(mtds[0].string)
                match_content.append(mtds[1].contents[0].string)
                mhref = mtds[2].find(name="a")["href"]
                match_content.append(re.search('\d+', mhref).group(0))
                match_content.append(mhref)
                teams = mtds[2].contents[0].string.split(' VS ')
                match_content.append(teams[0])
                match_content.append(teams[1])
                match_content.append(mtds[3].string)
                matches_lst.append(dict(zip(match_title, match_content)))
        for index,m in enumerate(matches_lst):
            redir = "http://info.sporttery.cn/football/pool_result.php?id=" + m['mm']
            self.viewer.forward("", redir)
            self.viewer.getHtml()
            handicap_soup = BeautifulSoup(self.viewer.html)
            tables = handicap_soup.findAll(name="table")
            rangtable = tables[1]
            rang_lst = []
            for td in rangtable.findAll(name="tr")[-1].findAll(name="td"):
                rang_lst.append(td.contents[0].strip())
            shengtable = tables[2]
            sheng_lst = []
            for td in shengtable.findAll(name="tr")[-1].findAll(name="td"):
                sheng_lst.append(td.contents[0].strip())
            qiutable = tables[3]
            qiu_lst = []
            for td in qiutable.findAll(name="tr")[-1].findAll(name="td"):
                qiu_lst.append(td.contents[0].strip())
            bantable = tables[4]
            ban_lst = []
            for td in bantable.findAll(name="tr")[-1].findAll(name="td"):
                ban_lst.append(td.contents[0].strip())
            fentable = tables[5]
            fen_lst = []
            fentr = fentable.findAll(name="tr")
            fen_lst.append(fentr[-7].findAll(name="div")[-1].string.strip())
            for td in fentr[-5].findAll(name="td"):
                fen_lst.append(td.contents[0].strip())
            for td in fentr[-3].findAll(name="td"):
                fen_lst.append(td.contents[0].strip())
            for td in fentr[-1].findAll(name="td"):
                fen_lst.append(td.contents[0].strip())
            matches_lst[index]['rang'] = "/".join(rang_lst)
            matches_lst[index]['sheng'] = "/".join(sheng_lst)
            matches_lst[index]['qiu'] = "/".join(qiu_lst)
            matches_lst[index]['ban'] = "/".join(ban_lst)
            matches_lst[index]['fen'] = "/".join(fen_lst)
            try:
                # self.__record(matches_lst[index])
                self.__commitData(matches_lst[index])
            except Exception:
                ShowMsg.showMsgEndline("Error while saving data: %s" % (matches_lst[index]["mid"],))
                continue

    def __record(self, dictm):
        fp = codecs.open(r'/home/zz/Documents/matches_lst.data', 'a', 'utf-8')
        for k, v in dictm.iteritems():
            fp.write("%s: %s\n" % (k, v))
        fp.write("\n" + "#"*60 + "\n")
        fp.close()

    def __commitData(self, dictm):
        import sys,os
        sys.path.append('/home/wang/code/lottery/server/')
        os.environ['DJANGO_SETTINGS_MODULE']='server.settings'
        from football.models import Match,Odd,CurrentMatch
        ma = Match()
        ma.home = dictm["mhometeam"]
        ma.away = dictm["mawayteam"]
        ma.handicap = dictm["rang"].split("/")[1]
        ma.save()
        od = Odd()
        od.match = ma
        odd_info = " ".join(dictm["sheng"].split("/")[1:] + dictm["rang"].split("/")[2:] \
                        + dictm["qiu"].split("/")[1:] + dictm["ban"].split("/")[1:] \
                        + dictm["fen"].split("/")[1:])
        od.odd = odd_info
        od.save()
        cma = CurrentMatch()
        cma.match = ma
        cma.odd = od
        cma.save()