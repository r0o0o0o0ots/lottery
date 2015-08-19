# -*-coding:utf-8 -*-
__author__ = 'ZZ'
from viewer.HtmlViewer import HtmlViewer

def grabFootballMatch():
    # start at root website
    hw = HtmlViewer("www.sporttery.cn")
    hw.tryConnect()
    hw.getHtml()
    hw.forward(u"受注赛程")
    hw.getHtml()
    match_list = hw.analyse()
    for m in match_list:
        dir_uri = 'http://info.sporttery.cn/football/pool_result.php?id=%s' % (m['mid'],)
        hw.forward("###", dir_uri)
        hw.getHtml()
    hw.home()
    hw.back()


if __name__ == '__main__':
    grabFootballMatch()
