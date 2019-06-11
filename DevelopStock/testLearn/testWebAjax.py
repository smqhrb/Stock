import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import csv
import scipy
import re
import urllib.request as urllib2
import xlwt
from bs4 import BeautifulSoup 
from html.parser import HTMLParser  
from urllib import request
from urllib import parse
from urllib.request import urlopen

import json
from jsonpath import jsonpath #从jsonpath库中导入jsonpath方法

def getSSE(url):
    headers={
        'Referer': 'http://www.sse.com.cn/assortment/stock/list/share/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }


    req = urllib2.Request(url, headers = headers)
    try:
        content = urllib2.urlopen(req).read()
    except:
        return
    return content
def get10jqka(url,type='year'):
    '''
    同花顺获取数据
    http://basic.10jqka.com.cn/api/stock/finance/000002_debt.json #资产负债表
    http://basic.10jqka.com.cn/api/stock/finance/000002_benefit.json #利润表
    http://basic.10jqka.com.cn/api/stock/finance/000002_cash.json #现金流量表
    http://basic.10jqka.com.cn/api/stock/finance/000002_each.json # 主要指标 每股能力
    http://basic.10jqka.com.cn/api/stock/finance/000002_grow.json # 主要指标 成长能力
    http://basic.10jqka.com.cn/api/stock/finance/000002_pay.json  # 主要指标 偿债能力
    http://basic.10jqka.com.cn/api/stock/finance/000002_operate.json # 主要指标 运营能力

    '''
    headers={
    # 'Referer': 'http://basic.10jqka.com.cn/000002/finance.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'        
    }
    req = urllib2.Request(url, headers = headers)
    content = urllib2.urlopen(req).read()
    text =content.decode('utf8')
    jsonobj = json.loads(text)
    data =jsonobj['flashData']
    dataList =json.loads(data)
    title =dataList['title']
    for k in range(1,len(title),1):
        title[k]="%s(%s)"%(title[k][0] ,title[k][1])
    resultData =[]
    if(type=='year'):
        year  =dataList['year']#年报
        resultData =year
    else:
        report =dataList['report']#季报
        resultData =report
    df =pd.DataFrame(data=resultData,index=title)
    print(df.T)
    return df.T

# import json
# from jsonpath import jsonpath #从jsonpath库中导入jsonpath方法
# # 
# from selenium import webdriver
# from pyquery import PyQuery as pq
# # 
# def openurl(url):
#     brower =webdriver.Chrome()
#     brower.get(url)
   
#     html =brower.page_source
#     data =str(pq(html))
#     print(data)
#     dd =brower.find_element_by_class_name('top_thead')
if __name__ == '__main__':
    # tt =getSSE('http://query.sse.com.cn/security/stock/getStockListData2.do?&jsonCallBack=jsonpCallback98649&isPagination=true&stockCode=&csrcCode=&areaName=&stockType=1&pageHelp.cacheSize=1&pageHelp.beginPage=1&pageHelp.pageSize=25&pageHelp.pageNo=1&_=1559826448226')
    # print(tt)


    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_debt.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_benefit.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_cash.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_each.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_grow.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_pay.json')
    get10jqka('http://basic.10jqka.com.cn/api/stock/finance/000002_operate.json')