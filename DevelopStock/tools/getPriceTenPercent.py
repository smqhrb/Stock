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
import re
# stockHsUp ="http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up%s"
stockHsUp ="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=auto"
# stockHsUp ="http://hq.sinajs.cn/rn=b5zw4&amp;list=sz000630,sz002131,sz002505,sh600157,sh600139,sh601326,sz300043,sh600020,sz002610,sz300255,sh603011,sz300291,sh600293,sz000633,sh601598,sz002477,sh600552,sz002519,sh600868,sh600589,sh603111,sz002711,sh601016,sz000795,sh600736,sz002356,sh600651,sh601890,sz000607,sz002175,sh600572,sz002600,sz300352,sz000810,sz300293,sz002143,sz002316,sz300249,sz300081,sz300160%s"
class stockUpTenPercent:
    '''
    目标:近40天涨停股票 按文件单独存储到xls文件中
    输入:近40天涨停股票
    输出:换手率 成交量 流通市值 量比 涨跌幅,
        ma5 ma10 ma20 ma31 ma60 ma120 dif dea mace
        (ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
        m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率
    '''
    def __init__(self):
        pass
    def urlOpenContent(self,urlBase,urlfix=""):
        '''
        parameter:
            url is made by urlBase urlfix
        return content
        '''
        url =urlBase%(urlfix)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return 
        return content   
    def stock_hs_up(self,rcDay =40):
        content =self.urlOpenContent(stockHsUp,'1')
        # print(content)
   
        # content =content.decode('UTF-8','strict')
        # # content =content.decode()
        # text = json.loads(content)
        # print (text)
        soup = BeautifulSoup(content,features="lxml")
        print(soup.p.text)
        retContent = soup.p.text
        retContent =retContent.replace('symbol','"symbol"')
        retContent =retContent.replace('code','"code"')
        retContent =retContent.replace('name','"name"')
        retContent =retContent.replace('trade','"trade"')
        retContent =retContent.replace('pricechange','"pricechange"')
        retContent =retContent.replace('changepercent','"AA"')#?
        retContent =retContent.replace('buy','"buy"')
        retContent =retContent.replace('sell','"sell"')
        retContent =retContent.replace('settlement','"settlement"')
        retContent =retContent.replace('open','"open"')
        retContent =retContent.replace('high','"high"')
        retContent =retContent.replace('low','"low"')
        retContent =retContent.replace('volume','"volume"')
        retContent =retContent.replace('amount','"amount"')
        retContent =retContent.replace('ticktime','"ticktime"')
        retContent =retContent.replace('per','"per"')#
        retContent =retContent.replace('pb','"pb"')
        retContent =retContent.replace('mktcap','"mktcap"')
        retContent =retContent.replace('nmc','"nmc"')
        retContent =retContent.replace('turnoverratio','"turnoverratio"')
        retContent =retContent.replace('"AA"','"changepercent"')
        text = json.loads(retContent)
        pd.DataFrame(text)
        print(text)

        # text =re.findall(r"{(.+?)}",soup.p.text)
        # text = json.loads(soup.p.text)
        # print (text)
        # optionAll = soup.findAll("p")  #获取所有日期
        # optionAll = soup.findAll("script",{"id":"_s_qdl_xz_4"}) 
        # print(optionAll)


if __name__ == '__main__':
    Test =stockUpTenPercent()
    Test.stock_hs_up()

