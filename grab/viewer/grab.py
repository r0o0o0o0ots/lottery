# -*-coding:utf-8 -*-
__author__ = 'ZZ'
from viewer.HtmlViewer import HtmlViewer

hw = HtmlViewer("www.sporttery.cn")
hw.tryConnect()
hw.getHtml()
hw.forward(u"受注赛程")
hw.getHtml()
hw.analyse()
