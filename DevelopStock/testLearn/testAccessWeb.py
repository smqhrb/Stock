import getopt
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import urllib.request as urllib2
from bs4 import BeautifulSoup 
import random
from html.parser import HTMLParser
import time
import math
import json
import random
import lxml.html
from lxml import etree
from pandas.io.html import read_html
from pandas.compat import StringIO
import xlwt

import pandas
import sqlite3 as db
class RandomHeader:
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def GetHeader(self):
        headers={"User-Agent":random.choice(self.user_agent_list)}
        return headers
import time
import re
from pyquery import PyQuery as pq    
import re
import pandas as pd
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions as EC 
class dataOper:
    '''
    fetch_hist_data
    按日期 排序
    '''
    def __init__(self,db_file=""):
        self.db =dbOper(db_file)
    # 1.GetStockList
    def GetCodeList(self):
        '''
        #获取股票列表
        #code,代码 name,名称 
        ''' 
               
        if os.path.exists("stockListAccount.xls") is True:     #判断文件 stockList.xls 是否存在,如果存在 则从文件中读取
            print("------开始读取stockListAccount股票信息")
            self.df =pd.read_excel('stockListAccount.xls',dtype={'code':'str'})
            self.df =self.df.sort_values(by=['code'])
            self.df =self.df.set_index('code')
            
            print("------结束读取stockListAccount.xls股票信息")
        else:
            self.GetStockListFromNet()#不存在则从网上读取

        return self.df

    def GetStockListFromNet(self):
        print("------开始读取网上股票列表信息")
        self.df = ts.get_stock_basics()             
        self.df =self.df.sort_values(by=['code'])
        write = pd.ExcelWriter('stockListAccount.xls')     #存储到文件  stockList.xls  
        self.df.to_excel(write,index=True)
        write.save()
        print("------结束读取网上股票列表信息")

    def GetStockListFromSina(self):
        '''
        1.get all count
        2.every request 20 or 40 or 80
        3.get data
        '''
        everyPage =40
        print("------开始读取网上股票列表信息")   
        #get stock count
        # http://vip.stock.finance.sina.com.cn/mkt/#hs_a
        # http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hs_a 
        # 40 
        # http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=1&num=40&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=init
        getH =RandomHeader()
        headers =getH.GetHeader()
        url ="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeStockCount?node=hs_a"
        req = urllib2.Request(url, headers = headers)
        content = urllib2.urlopen(req).read()
        text =content.decode('utf8')
        # print(text)
        count =text[(text.find('("')+2):text.find('")')]
        # print(count)
        iCount =int(count)
        pageCount =math.ceil(iCount/everyPage)
        df =pd.DataFrame()
        for page in range(1,pageCount+1):
            data_url =("http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=%s&sort=symbol&asc=1&node=hs_a&symbol=&_s_r_a=init")%(page,everyPage)
            getH =RandomHeader()
            headers =getH.GetHeader()
            req = urllib2.Request(data_url, headers = headers)
            content = urllib2.urlopen(req).read()
            text =content.decode('GBK')
            text =self.jsonfy(text)# to dict 不带双引号的json的key标准化
            if(len(df)==0):
                df =pd.DataFrame(data=text)
            else:
                df1 =pd.DataFrame(data=text)
                df =df.append(df1)
                r = df1[['code','name']]
                self.db.to_sql(r,'stock_code_name')
            # self.db.to_sql(df,'stock_code_name')
            #write to db
            
            #
            # time.sleep(random.uniform(1.1,3.4) )
            time.sleep(random.random()+1)
        # write = pd.ExcelWriter('stockListAccount.xls')
        # # columns =['symbol','code','name','open','high','low','buy','amount','changepercent','mktcap','nmc','pb','per','pricechange','sell','settlement','trade','turnoverratio','volume','ticktime']
        # columns =['code','name']
        # df.to_excel(write,index=True,columns=columns)
        # write.save()
        print("------结束读取网上股票列表信息")   
    def jsonfy(self,s):
        #此函数将不带双引号的json的key标准化
        obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj 
    # 2.GetStockData open close pre_close pct_chg涨跌幅度
    def getStockDataInDifferentFileUser(self,stockCodeList,start,end):
        path ="./%sTo%s"%(start,end)
        if(os.path.exists(path)==False): #判断目标是否存在 
            os.mkdir(path) #创建目录
        pro = ts.pro_api()
        i=0
        for code in stockCodeList:
            savefileName =path+'/'+code+'('+start+'To'+end+').xlsx'
            i =i+1
            if(os.path.exists(savefileName)):
                print("...[%d]%s exist"%(i,savefileName))
                print("...reading fileName =%s"%savefileName)
                df1 = pd.read_excel(savefileName)
                df1.rename(columns={'股票代码':'ts_code','交易日期':'trade_date','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','昨收价':'pre_close','涨跌额':'change','涨跌幅(未复权)':'pct_chg','成交量 （手）':'vol','成交额(千元)':'amount'}, inplace = True)
                # df=df1.sort_values(by=['trade_date'])
                df =df1
            else:
                time.sleep(0.3)
                print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
                # df =ts.get_hist_data(code,start=start,end=end)
                # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

                df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
                df=df1.sort_values(by=['trade_date'])
                df=df.reset_index()
                df.drop(['index'],axis=1,inplace=True)
            ####
            #比如002321这份数据 第71行（2018年6月1日）
            # 最高价等于昨收价的1.1倍（四舍五入）
            # 并且6月1日的最高价未高于其前5个交易的最高价（即前5个交易日有价格高于6月1日的最高价即可）  
            # 数据符合条件 然后在该行后标记个1，在其后面一行（72行）标记为2   
            # 做标记的目的是方便筛选
            

            df_temp =df[round(df['high']/df['pre_close'],2)==1.1]
            df['flag']=''
            for j in range(len(df_temp)):
                ind =df_temp.index[j]
                if(ind>5):
                    value =df.iloc[ind]['high']
                    if((df.iloc[ind-1]['high']>=value) or (df.iloc[ind-2]['high']>=value) or (df.iloc[ind-3]['high']>=value) or (df.iloc[ind-4]['high']>=value)  or (df.iloc[ind-5]['high']>=value)):
                        df.loc[ind,'flag'] =1
                        df.loc[ind+1,'flag']=2        
            ####
            df['最高涨幅'] =df['high']/df['pre_close'] -1
            df['最低涨幅'] =df['low']/df['pre_close'] -1
            df['收盘涨幅'] =df['close']/df['pre_close'] -1
            df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
            order =['股票代码','交易日期','开盘价','最高价','最高涨幅','最低价','最低涨幅','收盘价','收盘涨幅','昨收价','涨跌额','涨跌幅(未复权)','成交量 （手）','成交额(千元)','flag']
            dfR =df[order]
            writer = pd.ExcelWriter(savefileName)
            dfR.to_excel(writer,sheet_name=code)

            writer.save()
            print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))
    # 3.StoreToDB

    # 4.GetGpFxrq

    def GetGpFxrq(self,Code):
        # http://stockpage.10jqka.com.cn/000600/company/
        getH =RandomHeader()
        headers =getH.GetHeader()
        url ="http://basic.10jqka.com.cn/000600/company.html#stockpage"
        req = urllib2.Request(url, headers = headers)
        content = urllib2.urlopen(req).read()
        # text =content.decode('utf8')
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        # div0 = soup.find("div",{"class":"m_box company_detail"})
        div0 = soup.find("table",{"class":"cnhk-cf tblM s4 s5 type2 mar15T"})
        dbrow =div0.findAll("tr")       
        pass
        # options=webdriver.ChromeOptions()
        # options.add_argument('--ignore-certificate-errors')
        # browser=webdriver.Chrome(chrome_options=options)     
        # browser.get("http://basic.10jqka.com.cn/000600/company.html#stockpage")                 #进入相关网站
        # # html=browser.page_source #获取网站源码
        # # 大型水库的数据表--xpath
        # # water_table_xpath = "//*[@id=\"sktable\"]/table/tbody"
        # water_table_xpath = "//*[@id=\"publish\"]/div[2]/table/tbody/tr[2]/td[1]/span"
        # # 得到新的页面，并等待其数据表加载完成
        # wait = WebDriverWait(browser, 50)
        # wait.until(EC.presence_of_element_located(
        #     (By.XPATH, water_table_xpath)))   
        # soup = BeautifulSoup(browser.page_source, 'lxml')   
        # table0 = soup.find("div",{"class":"m_box company_detail"})  
        # # data=str(pq(html)) #str() 函数将对象转化为适于人阅读的形式。  
        # # soup = BeautifulSoup(data,features="lxml") 
        

        # dic={}
        # re_rule=r'<div class="m_box company_detail" id="publish" stat="company_publish">(.*?)</div>'
        # datalist=re.findall(re_rule,data,re.S)
        # print(datalist)               
if __name__ == '__main__':
    # https://github.com/sadjjk/tonghuashun_industry
    # https://www.jianshu.com/p/13381aac9245
    test =dataOper("stockA.db")
    # test.GetStockListFromSina()
    test.GetGpFxrq("000600")

# https://www.legulegu.com/
# http://basic.10jqka.com.cn/000600/company.html#stockpage