#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:中央气象局天气预报城市Code爬虫
Created on 2016/09/27
@author: wang.zheng@ctrip.com
@version: 0.1
'''
import threading
import os
import sys
import re
import json
import time
import urllib
import urllib2
import cookielib
import random
from bs4 import BeautifulSoup
import lxml.html
from collections import defaultdict
from pprint import pprint
from config import provinces,provincesCitys,cityInfoDict,cityCodeDict
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
import socket
socket.setdefaulttimeout(timeout)

class BrowserOpener:
    def myopener(self):
        cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
        opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        user_agents = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "]
        agent = random.choice(user_agents)
        opener.addheaders = [("User-agent", agent), ("Accept", "*/*"), ('Referer', 'http://www.baidu.com')]
        return opener


class CityInfoSpider(BrowserOpener):
    def __init__(self):
        self.opener = self.myopener()

    def getCityCode(self,province):
        initUrl = "http://www.nmc.cn/f/rest/province/%s"%(province)
        #time.sleep(random.uniform(1, 3))
        infoTmpDict = defaultdict(dict)
        codeTmpDict = defaultdict(list)
        htmlContents = self.opener.open(initUrl).read()
        pat = province + r'/(.+)+.html'
        for item in eval(htmlContents):
            url = item.get("url")
            cityEN = re.search(pat, str(url)).group(1)
            cityCN = item.get("city")
            cityCode = item.get("code")
            infoTmpDict[province][cityCode]=[cityCN,cityEN,url]
            codeTmpDict[province].append(cityCode)
        return infoTmpDict,codeTmpDict
def main():
    ccs = CityInfoSpider()
    for pro in provinces.iterkeys():
        cityInfoDict.update(ccs.getCityCode(pro)[0])
        cityCodeDict.update(ccs.getCityCode(pro)[1])
    json.dump(cityInfoDict, open("cityInfo.json", "w"), encoding="utf-8", ensure_ascii=False)
    json.dump(cityCodeDict, open("cityCode.json", "w"), encoding="utf-8", ensure_ascii=False)

if __name__ == '__main__':
    main()