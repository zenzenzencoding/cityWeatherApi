#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:�����������������ļ�
Created on 2016/09/27
@author: wang.zheng@ctrip.com
@version: 0.1
'''
from collections import defaultdict
#��������
provinces = {
"ABJ":"������",
"ATJ":"�����",
"AHE":"�ӱ�",
"ASX":"ɽ��",
"ANM":"���ɹ�",
"ALN":"����",
"AJL":"����",
"AHL":"������",
"ASH":"�Ϻ���",
"AJS":"����",
"AZJ":"�㽭",
"AAH":"����",
"AFJ":"����",
"AJX":"����",
"ASD":"ɽ��",
"AHA":"����",
"AHB":"����",
"AHN":"����",
"AGD":"�㶫",
"AGX":"����",
"AHI":"����",
"ACQ":"������",
"ASC":"�Ĵ�",
"AGZ":"����",
"AYN":"����",
"AXZ":"����",
"ASN":"����",
"AGS":"����",
"AQH":"�ຣ",
"ANX":"����",
"AXJ":"�½�",
"AXG":"���",
"AAM":"����",
"ATW":"̨��"
}

provincesCitys= {}
realWeatherDict = defaultdict(dict)
forecastWeatherDict = defaultdict(dict)
cityInfoDict = defaultdict(dict)
cityCodeDict = defaultdict(list)


