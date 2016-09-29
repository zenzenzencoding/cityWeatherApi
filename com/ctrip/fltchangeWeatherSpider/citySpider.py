#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:城市信息爬虫
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
from config import provinces,provincesCitys
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
import socket

socket.setdefaulttimeout(timeout)

class BrowserOpener:
    def __init__(self):
        self.url_init = "http://www.nmc.cn/publish/forecast/ASH/pudong.html"

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


class CitySpider(BrowserOpener):
    def __init__(self,province):
        self.province = province
        self.initUrl = "http://www.nmc.cn/publish/forecast/%s.html"%(province)
        self.opener = self.myopener()

    def getCitys(self):
        time.sleep(random.uniform(1, 5))
        cityDict = {self.province:[]}
        try:
            html_text = self.opener.open(self.initUrl).read()
            soup = BeautifulSoup(html_text, "lxml")
            item_soup = soup.find('div', {'id': "areaContent"})
            if item_soup is None:
                return cityDict
        except Exception, e:
            print Exception, ":", e
        try:
            items_html = item_soup.findAll('div', {'class': "cname"})
        except Exception, e:
            print Exception, ":", e
        for item_html in items_html:
            try:
                pat = self.province + r'/(.+)+.html'
                cityName = item_html.find('a').get('href')
                _cityNameEN = re.search(pat, str(cityName))
                print _cityNameEN.group(0)
                print _cityNameEN.group(1)
                cityNameEN = _cityNameEN.group(1)
                cityNameCN = item_html.find('a').string
                #print cityNameCN.decode("utf-8")
            except Exception, e:
                print Exception, ":", e
                continue
            cityDict[self.province].append((cityNameEN,cityNameCN.decode("utf-8")))
        return cityDict

if __name__ == '__main__':
    for pro in provinces:
        csp = CitySpider(pro)
        cd = csp.getCitys()
        provincesCitys.update(cd)
    #pprint(provincesCitys)
    json.dump(provincesCitys,open("provincesCitys.json","w"),encoding="utf-8",ensure_ascii=False)

