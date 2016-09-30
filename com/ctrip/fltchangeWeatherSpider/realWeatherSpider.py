#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:城市实时天气爬虫
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
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
import socket
socket.setdefaulttimeout(timeout)
import chardet
import pandas as pd
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

class RealWeatherSpider(BrowserOpener):
    def __init__(self):
        self.opener = self.myopener()

    def getRealCityWeather(self,cityCode):
        initUrl = r"http://www.nmc.cn/f/rest/real/%s"%(cityCode)
        contents = self.opener.open(initUrl).read()
        typeEncode = sys.getfilesystemencoding()  #系统默认编码
        infoencode = chardet.detect(contents).get('encoding', 'utf-8')  #提取网页的编码
        realWeatherInfo = eval(contents.decode(infoencode, 'ignore').encode(typeEncode))  #先转换成unicode编码 然后转换系统编码输出
        city = realWeatherInfo["station"]["city"]
        publishDate = realWeatherInfo["publish_time"].split()[0]
        publishTime = realWeatherInfo["publish_time"].split()[1]
        temperature = realWeatherInfo["weather"]["temperature"]
        humidity = realWeatherInfo["weather"]["humidity"]
        rain = realWeatherInfo["weather"]["rain"]
        rcomfort = realWeatherInfo["weather"]["rcomfort"]
        weatherType = realWeatherInfo["weather"]["info"]
        windDirect = realWeatherInfo["wind"]["direct"]
        windPower = realWeatherInfo["wind"]["power"]
        windSpeed = realWeatherInfo["wind"]["speed"]
        _realWeather={"city":city,
                       "cityCode":[cityCode],
                       "publishDate":[publishDate],
                       "publishTime":[publishTime],
                       "temperature":[temperature],
                       "humidity":[humidity],
                       "rain":[rain],
                       "rcomfort":[rcomfort],
                       "weatherType":[weatherType],
                       "windDirect": [windDirect],
                       "windSpeed":[windSpeed],
                       "windPower":[windPower]}
        return pd.DataFrame(_realWeather)
def main():
    from config import realWeather
    print realWeather
    ctime = time.strftime("%Y%m%d", time.localtime(time.time()))
    cityCodes =json.load(open("cityCode.json","r"),encoding="utf-8")
    rws = RealWeatherSpider()
    for pro in cityCodes:
        for cc in cityCodes.get(pro):
            realWeather = pd.concat([realWeather,rws.getRealCityWeather(cc)],ignore_index=True)
    realWeather.to_csv("realtWeather_%s" % (ctime), index=False)
    print realWeather

if __name__ == '__main__':
    main()


