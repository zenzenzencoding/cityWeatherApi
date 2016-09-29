#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:航变天气爬虫配置文件
Created on 2016/09/27
@author: wang.zheng@ctrip.com
@version: 0.1
'''
from collections import defaultdict
#地区配置
provinces = {
"ABJ":"北京市",
"ATJ":"天津市",
"AHE":"河北",
"ASX":"山西",
"ANM":"内蒙古",
"ALN":"辽宁",
"AJL":"吉林",
"AHL":"黑龙江",
"ASH":"上海市",
"AJS":"江苏",
"AZJ":"浙江",
"AAH":"安徽",
"AFJ":"福建",
"AJX":"江西",
"ASD":"山东",
"AHA":"河南",
"AHB":"湖北",
"AHN":"湖南",
"AGD":"广东",
"AGX":"广西",
"AHI":"海南",
"ACQ":"重庆市",
"ASC":"四川",
"AGZ":"贵州",
"AYN":"云南",
"AXZ":"西藏",
"ASN":"陕西",
"AGS":"甘肃",
"AQH":"青海",
"ANX":"宁夏",
"AXJ":"新疆",
"AXG":"香港",
"AAM":"澳门",
"ATW":"台湾"
}

provincesCitys= {}
realWeatherDict = defaultdict(dict)
forecastWeatherDict = defaultdict(dict)
cityInfoDict = defaultdict(dict)
cityCodeDict = defaultdict(list)


