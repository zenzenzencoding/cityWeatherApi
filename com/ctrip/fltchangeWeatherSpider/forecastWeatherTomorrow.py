#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:城市天气爬虫(t+1预报) 每天06:00分执行
Created on 2016/09/27
@author: wang.zheng@ctrip.com
@version: 0.1
'''
import pandas as pd
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
from config import provinces,provincesCitys,realWeatherDict,forecastWeatherTomorrow
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
        _forecastWeatherTomorrow = {}
        contents = urllib2.urlopen(req).read()
        typeEncode = sys.getfilesystemencoding()  #系统默认编码
        infoencode = chardet.detect(contents).get('encoding', 'utf-8') #提取网页的编码
        htmlContents = contents.decode(infoencode, 'ignore').encode(typeEncode)
        sites = etree.HTML(contents)
        ptimeTomorrow =[str(re.search(r"\d+:{1}\d+",item.strip()).group(0)) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row first"]/div/text()')[1:]]
        tqxxTomorrow= [ str(re.search(r"day/(\d+).png",item).group(1)) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row second tqxx"]//img/@src')]
        wdTomorrow = [str(re.search(r"([-+]*\d+\.*\d*)",item.strip()).group(1)) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row wd"]/div/text()')[1:]]
        _jsTomorrow = [item.strip() for item in sites.xpath('//body//div[@id="day1"]/div[@class="row js"]/div/text()')[1:]]
        jsTomorrow = []
        for item in _jsTomorrow:
            try:
                js = str(re.search(r"([-+]*\d+\.*\d*)", item.strip()).group(1))
            except Exception, e:
                print Exception, ":", e
                js = "0"
                continue
            finally:
                jsTomorrow.append(js)
        speedTomorrow = [str(re.search(r"([-+]*\d+\.*\d*)",item.strip()).group(1)) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row winds"]/div/text()')[1:]]
        winddTomorrow = [str(item.strip()) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row windd"]/div/text()')[1:]]
        xdsdTomorrow = [str(item.strip().split("%")[0]) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row xdsd"]/div/text()')[1:]]
        ylTomorrow = [str(item.strip().split("%")[0]) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row yl"]/div/text()')[1:]]
        _njdTomorrow = [str(item.strip()) for item in sites.xpath('//body//div[@id="day1"]/div[@class="row njd"]/div/text()')[1:]]
        njdTomorrow = []
        for item in _njdTomorrow:
            try:
                njd = str(re.search(r"([-+]*\d+\.*\d*)", item.strip()).group(1))
            except Exception, e:
                print Exception, ":", e
                njd = "-999" # -999 表示缺失值
                continue
            finally:
                njdTomorrow.append(njd)
        _forecastWeatherTomorrow ={
            "city":[city]*8,
            "createdate":[self.time]*8,
            "forecasttime":ptimeTomorrow,
            "tqxx":tqxxTomorrow,
            "wd":wdTomorrow,
            "js":jsTomorrow,
            "speed":speedTomorrow,
            "windd":winddTomorrow,
            "xdsd":xdsdTomorrow,
            "yl":ylTomorrow,
            "njd":njdTomorrow
        }
        return pd.DataFrame(_forecastWeatherTomorrow)

if __name__ == '__main__':
    fws = ForecastWeatherSpider()
    cityInfo =json.load(open("cityInfo.json","r"),encoding="utf-8")
    ctime = time.strftime("%Y%m%d", time.localtime(time.time()))
    for pro in cityInfo:
        for cc in cityInfo.get(pro):
            cityname = cityInfo[pro][cc][1]
            forecastWeatherTomorrow = pd.concat([forecastWeatherTomorrow, fws.getForecastWeather(pro, cityname)],
                                             ignore_index=True)
    forecastWeatherTomorrow.to_csv("forecastWeatherTomorrow_%s" % (ctime), index=False)



