#!/usr/bin/env python
#-*-coding:utf-8-*-
'''
Description:
Created on 2016年09月30日
@author: zenwan
@version: 
'''
import re
import json
import chardet
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import urllib2
from lxml import etree
import lxml.html.soupparser as soupparser
if __name__ == '__main__':
    initUrl = "http://www.nmc.cn/publish/forecast/ASH/pudong.html"
    req = urllib2.Request(initUrl, headers={"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"})
    contents = urllib2.urlopen(req).read()
    #sites = soupparser.fromstring(contents)





