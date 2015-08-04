# -*-coding:utf-8-*-
__author__ = 'zz'
import re

class Graber:

    @staticmethod
    def grabAll(regex, content):
        matcher = re.compile(regex)
        result_lst = []
        for matched_lst in matcher.findall(content):
            result_lst.append(matched_lst)
        return result_lst

    @staticmethod
    def group(regex, content, index):
        matcher = re.compile(regex)
        return matcher.match(content).group(index)