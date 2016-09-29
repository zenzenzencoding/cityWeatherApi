#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:������������(t and t+1Ԥ��) ÿ��00:00��ִ��
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
from config import provinces,provincesCitys,realWeatherDict
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
import socket
socket.setdefaulttimeout(timeout)
import chardet
from lxml import etree
class ForecastWeatherSpider():

    def getForecastWeather(self,pro,city):
        #time.sleep(random.uniform(1, 5))
        self.initUrl = "http://www.nmc.cn/publish/forecast/%s/%s.html"%(pro,city)
        req = urllib2.Request(self.initUrl,headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"})
        _forecastWeatherToday = defaultdict(dict)
        _forecastWeatherTomorrow = defaultdict(dict)
        contents = urllib2.urlopen(req).read()
        typeEncode = sys.getfilesystemencoding()  #ϵͳĬ�ϱ���
        infoencode = chardet.detect(contents).get('encoding', 'utf-8') #��ȡ��ҳ�ı���
        htmlContents = contents.decode(infoencode, 'ignore').encode(typeEncode)
        sites = etree.HTML(contents)
        day0_ = sites.xpath('//body//div[@id="day0"]/div[@class="row windd"]/div/text()')
        for item in day0:
            print item.strip()

if __name__ == '__main__':
    fws = ForecastWeatherSpider()
    fws.getForecastWeather("ASH","pudong")


