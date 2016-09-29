#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:城市天气爬虫(t预报) 每天00:00分执行
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
from config import provinces,provincesCitys,realWeatherDict,forecastWeatherToday
reload(sys)
sys.setdefaultencoding('utf-8')
timeout = 20
import socket
socket.setdefaulttimeout(timeout)
import chardet
from lxml import etree
class ForecastWeatherSpider():
    def __init__(self):
        self.time = time.strftime("%Y%m%d",time.localtime(time.time()))

    def getForecastWeather(self,pro,city):
        #time.sleep(random.uniform(1, 5))
        self.initUrl = "http://www.nmc.cn/publish/forecast/%s/%s.html"%(pro,city)
        req = urllib2.Request(self.initUrl,headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"})
        _forecastWeatherToday = defaultdict(dict)
        contents = urllib2.urlopen(req).read()
        typeEncode = sys.getfilesystemencoding()  #系统默认编码
        infoencode = chardet.detect(contents).get('encoding', 'utf-8') #提取网页的编码
        htmlContents = contents.decode(infoencode, 'ignore').encode(typeEncode)
        sites = etree.HTML(contents)
        ptimeToday =[item.strip() for item in sites.xpath('//body//div[@id="day0"]/div[@class="row first"]/div/text()')[1:]]
        tqxxToday= [ str(re.search(r"day/(\d+).png",item).group(1)) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row second tqxx"]//img/@src')]
        wdToday = [str(re.search(r"([-+]*\d+\.*\d*)",item.strip()).group(1)) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row wd"]/div/text()')[1:]]
        _jsToday = [item.strip() for item in sites.xpath('//body//div[@id="day0"]/div[@class="row js"]/div/text()')[1:]]
        jsToday = []
        for item in _jsToday:
            try:
                js = str(re.search(r"([-+]*\d+\.*\d*)", item.strip()).group(1))
            except Exception, e:
                print Exception, ":", e
                js = "0"
                continue
            finally:
                jsToday.append(js)
        speedToday = [str(re.search(r"([-+]*\d+\.*\d*)",item.strip()).group(1)) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row winds"]/div/text()')[1:]]
        winddToday = [str(item.strip()) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row windd"]/div/text()')[1:]]
        xdsdToday = [str(item.strip().split("%")[0]) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row xdsd"]/div/text()')[1:]]
        ylToday = [str(item.strip().split("%")[0]) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row yl"]/div/text()')[1:]]
        _njdToday = [str(item.strip()) for item in sites.xpath('//body//div[@id="day0"]/div[@class="row njd"]/div/text()')[1:]]
        njdToday = []
        for item in _njdToday:
            try:
                njd = str(re.search(r"([-+]*\d+\.*\d*)", item.strip()).group(1))
            except Exception, e:
                print Exception, ":", e
                njd = "-999" # -999 表示缺失值
                continue
            finally:
                njdToday.append(njd)
        _forecastWeatherToday[city][self.time]={
            "ptimeToday":ptimeToday,
            "tqxxToday":tqxxToday,
            "wdToday":wdToday,
            "jsToday":jsToday,
            "speedToday":speedToday,
            "winddToday":winddToday,
            "xdsdToday":xdsdToday,
            "ylToday":ylToday,
            "njdToday":njdToday
        }
        return _forecastWeatherToday


if __name__ == '__main__':
    fws = ForecastWeatherSpider()
    cityInfo =json.load(open("cityInfo.json","r"),encoding="utf-8")
    for pro in cityInfo:
        for cc in cityInfo.get(pro):
            cityname = cityInfo[pro][cc][1]
            forecastWeatherToday.update(fws.getForecastWeather(pro,cityname))


