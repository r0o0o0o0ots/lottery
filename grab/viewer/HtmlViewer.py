# -*-coding:utf-8-*-
__author__ = 'zz'
from urllib import urlopen
from time import sleep
import random
import socket
from ShowMsg import ShowMsg
from MatchMatches import MatchMatches
from Graber import Graber

class HtmlViewer:

    def __init__(self, theURI):
        if theURI.startswith("http://") or theURI.startswith("https://"):
            self.URI = theURI
        else:
            self.URI = "http://" + theURI
        self.conn = None
        self.history_URI = []
        self.html = u""
        socket.setdefaulttimeout(30)

    def connect(self):
        try:
            self.conn = urlopen(self.URI)
            return True
        except Exception:
            return False

    def tryConnect(self, try_times=3, with_no_wait=False):
        conn_return = False
        while try_times > 0:
            ShowMsg.showMsg("Try to connect '%s'..." % (self.URI,))
            if not with_no_wait:
                sleep(random.randint(3, 5))
            conn_return = self.connect()
            if conn_return:
                ShowMsg.showMsgEndline("\t successful.")
                break
            else:
                try_times = try_times-1
                ShowMsg.showMsgEndline("\t failed, try again, %d time(s) left." % (try_times))
        if conn_return:
            ShowMsg.showMsgEndline("Connection created.")
        else:
            ShowMsg.showMsgEndline("Please check URI: %s" % (self.URI,))
        if not with_no_wait:
            sleep(2)

    def getHtml(self, try_times=3, with_no_wait=False, webcoding="gbk"):
        get_falg = False
        while try_times > 0:
            try:
                ShowMsg.showMsg("Try to get html from website...")
                if not with_no_wait:
                    sleep(random.randint(3, 5))
                self.html = unicode(self.conn.read(), webcoding)
                get_falg = True
                ShowMsg.showMsgEndline("\t successful")
                break
            except Exception:
                try_times = try_times - 1
                ShowMsg.showMsgEndline("\t failed, try again, %d time(s) left." % (try_times,))
                continue
        if not get_falg:
            self.html = u""
        if not with_no_wait:
            sleep(2)

    def closeConnection(self):
        if not self.conn == None:
            self.conn.close()

    def home(self, home_URI='http://www.sporttery.cn'):
        ShowMsg.showMsgEndline("Redirect to home.")
        self.closeConnection()
        self.history_URI = []
        self.URI = home_URI
        self.tryConnect()

    def forward(self, theLinkName, theLink=""):
        if theLink == "":
            match_flag = False
            link_lst = Graber.grabAll('<a\s+href="(.*?)".*?>%s</a>' % (theLinkName,), self.html)
            for link in link_lst:
                if 'football' in link or 'fb_' in link:
                    self.history_URI.append(self.URI)
                    self.closeConnection()
                    self.URI = link
                    self.tryConnect()
                    match_flag = True
                    break
            if not match_flag:
                ShowMsg.showMsgEndline("Could not find link.")
        else:
            self.history_URI.append(self.URI)
            self.closeConnection()
            self.URI = theLink
            self.tryConnect()

    def back(self):
        if len(self.history_URI) <= 0:
            ShowMsg.showMsgEndline("Start page, cannot go back.")
        else:
            self.closeConnection()
            self.URI = self.history_URI.pop()
            self.tryConnect()

    def analyse(self, info_type='match_list'):
        if info_type == 'match_list':
            mm = MatchMatches()
            return mm.matchLists(self.html)
        elif info_type == 'match_result':
            pass
        elif info_type == 'match_live':
            pass
        else:
            ShowMsg.showMsgEndline("Unknown info type '%s'" % (info_type,))
            return []
