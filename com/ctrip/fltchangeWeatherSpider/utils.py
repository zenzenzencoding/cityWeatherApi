#!/usr/bin/ python
# -*-coding:utf-8-*-
'''
Description:
Created on 2016/09/27
@author: wang.zheng@ctrip.com
@version: 0.1
'''
import MySQLdb
from sqlalchemy import create_engine
import pandas as pd
def windLevel(windSpeed):
    wl=2
    if windSpeed =="微风"or windSpeed <= 3.3:
        wl = 2
    elif windSpeed >= 3.4 and windSpeed <= 5.4:
        wl = 3
    elif windSpeed >= 5.5 and windSpeed <= 7.9:
        wl = 4
    elif windSpeed >=8.0 and windSpeed<= 10.7:
        wl = 5
    elif windSpeed >=10.8 and windSpeed<=13.8:
        wl = 6
    elif windSpeed >=13.9 and windSpeed <= 17.1:
        wl = 7
    elif windSpeed>=17.2 and windSpeed<=20.7:
        wl = 8
    elif windSpeed>=20.8 and windSpeed<=24.4:
        wl = 9
    elif windSpeed>=24.5 and windSpeed<=28.4:
        wl = 10
    elif windSpeed>=28.5 and windSpeed<=32.6:
        wl = 11
    elif windSpeed>=32.7 and windSpeed<= 36.9:
        wl = 12
    elif windSpeed >37.0:
        wl = 13
    return wl-2

def data2sql(df):
    engine = create_engine('mysql+mysqlconnector://root:ecnu20142014@202.120.87.243:3306/zendata')
    #con = MySQLdb.connect("202.120.87.243","root","ecnu2014","zendata")
    df.to_sql("realweather",engine,if_exists="append",index=False)




