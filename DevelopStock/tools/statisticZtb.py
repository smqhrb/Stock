# 8个指标分别是
# 1.（A股收盘价低于-5%家数）-（跌停板家数），
# 2.A股最高板板数，
# 3.涨停板数量+涨停板被砸(最高价=涨停价，收盘价不等于涨停价)数量，
# 4.涨停板的（昨日涨停价-今日收盘价）/昨日涨停价的平均值，
# 5.涨停板被砸的（昨日涨停价-今日收盘价）/昨日涨停价的平均值，（最高价=涨停价，收盘价不等于涨停价）
# 6.1板的数量，
# 7.昨日1板的（昨日涨停价-今日收盘价）/昨日涨停价的平均值，
# 8.今日2板数量除以昨日1板数量

# 什么叫最高板 ：所有的涨停板里连板次数最多的（新股没开板的不计算在内）
# 这些数量里全是一字板的也丢掉

#using pysqlite 存储历史数据
#coding=utf-8
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
# from sqlalchemy import create_engine
# engine = create_engine(
#     "mysql+pymysql://root:root@localhost:3306/tushare?charset=utf8")
    
class dbOper:
    # https://www.cnblogs.com/lizunicon/p/4306730.htm
    # http://docs.jinkan.org/dodbOpercs/flask/patterns/sqlalchemy.html
    # https://www.cnblogs.com/zenan/p/10176767.html
    def __init__(self,db_file=""):
        # self.engine = create_engine('sqlite:///.\\%s'%db_file)
        self.cx = db.connect(db_file)
        
        # self.engine.connect(db_file)
    def cx_data(self,sql_select):
        cur =self.cx.cursor()
        cur.execute(sql_select)
        df =pd.DataFrame(cur.fetchall())
        cur.close()
        return df
    def update_data(self,sql_update):
        cur =self.cx.cursor()
        cur.execute(sql_update)
        cur.close()
        self.cx.commit()
    def pandas_tosql(self,df,tbl_name,ifexist):
        # df.to_sql(name = 'employee', con = con, if_exists='replace', index = None)
        df.to_sql(name = tbl_name, con = self.cx, if_exists=ifexist, index = None)
    # def test(self):
    #     self.update_data("insert into stock_code_name(code,name) values(\'000001\',\'pingan\');")
    #     self.update_data("insert into stock_code_name(code,name) values(\'000002\',\'pingan\');")
    #     self.update_data("insert into stock_code_name(code,name) values(\'000003\',\'pingan\');")

    def to_sql(self,dataf,tbl):
        '''
        dataf:存入数据的DataFrame
        tbl：数据库表名
        '''
        rowCnt =len(dataf)
        # dataf.to_sql(name=tbl,con=self.cx,if_exists='append',index= False)

        for i in range(rowCnt):
            try: 
                dataf.iloc[i:i+1].to_sql(name =tbl,  con=self.cx, if_exists='append',index= False)

                # self.cx.commit()
            except Exception as e:
                pass#
                # print('Error is ' + str(e))
                #self.con.rollback()   

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
                df1['sssj'] =""
                len_df1 = len(df1)
                for i in range(len_df1):
                    sssj =self.GetGpFxrq(df1['code'][i])
                    print('code=%s,date%s'%(df1['code'][i],sssj))
                    df1['sssj'][i]=sssj
                    time.sleep(random.random()+1)
                # df =df.append(df1)
                r = df1[['code','name','sssj']]
                self.db.to_sql(r,'stock_code_name')
            time.sleep(random.random()+1)

        print("------结束读取网上股票列表信息")   
    def jsonfy(self,s):
        #此函数将不带双引号的json的key标准化
        obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj 
    # 2.GetStockData open close pre_close pct_chg涨跌幅度
    def getStockDataInDifferentFileUser(self,start,end):
        pro = ts.pro_api()
        i=0
        df_sssj =self.db.cx_data("select code,sssj from stock_code_name where name not like '%ST%'")
        len_df =len(df_sssj)
        for k in range(len_df):
            #ts must delay 300ms
            time.sleep(0.3)
            #1 最后日期
            code =df_sssj[0][k]
            if code>='600000':
                code ="%s.SH"%code
            else:
                code ="%s.SZ"%code
            df_date =self.db.cx_data("select max(trade_date) as tdate from stock_day where ts_code =\'%s\'"%code)
            if(df_date[0][0]==None):
                start =df_sssj[1][k]
                if(start==""):
                    start ='20000101'
            else:
                start =df_date[0][0]
            # 
            dateTime_p = datetime.datetime.strptime(start,'%Y-%m-%d')
            start =datetime.datetime.strftime(dateTime_p,'%Y%m%d')
            now_time = datetime.datetime.now()#现在
            end =now_time.strftime('%Y%m%d')
            #2 重最后日期 到 最新日期的股价

            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df=df1.sort_values(by=['trade_date'])
            df=df.reset_index()
            df.drop(['index'],axis=1,inplace=True)
            #3 插入数据库
            self.db.to_sql(df,'stock_day')
            # i =i+1
            # if(os.path.exists(savefileName)):
            #     print("...[%d]%s exist"%(i,savefileName))
            #     print("...reading fileName =%s"%savefileName)
            #     df1 = pd.read_excel(savefileName)
            #     df1.rename(columns={'股票代码':'','交易日期':'trade_date','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','昨收价':'pre_close','涨跌额':'change','涨跌幅(未复权)':'pct_chg','成交量 （手）':'vol','成交额(千元)':'amount'}, inplace = True)
            #     # df=df1.sort_values(by=['trade_date'])
            #     df =df1ts_code
            # else:
            #     time.sleep(0.3)
            #     print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
            #     # df =ts.get_hist_data(code,start=start,end=end)
            #     # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

            #     df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            #     df=df1.sort_values(by=['trade_date'])
            #     df=df.reset_index()
            #     df.drop(['index'],axis=1,inplace=True)
            # ####
            # #比如002321这份数据 第71行（2018年6月1日）
            # # 最高价等于昨收价的1.1倍（四舍五入）
            # # 并且6月1日的最高价未高于其前5个交易的最高价（即前5个交易日有价格高于6月1日的最高价即可）  
            # # 数据符合条件 然后在该行后标记个1，在其后面一行（72行）标记为2   
            # # 做标记的目的是方便筛选
            

            # df_temp =df[round(df['high']/df['pre_close'],2)==1.1]
            # df['flag']=''
            # for j in range(len(df_temp)):
            #     ind =df_temp.index[j]
            #     if(ind>5):
            #         value =df.iloc[ind]['high']
            #         if((df.iloc[ind-1]['high']>=value) or (df.iloc[ind-2]['high']>=value) or (df.iloc[ind-3]['high']>=value) or (df.iloc[ind-4]['high']>=value)  or (df.iloc[ind-5]['high']>=value)):
            #             df.loc[ind,'flag'] =1
            #             df.loc[ind+1,'flag']=2        
            # ####
            # df['最高涨幅'] =df['high']/df['pre_close'] -1
            # df['最低涨幅'] =df['low']/df['pre_close'] -1
            # df['收盘涨幅'] =df['close']/df['pre_close'] -1
            # df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
            # order =['股票代码','交易日期','开盘价','最高价','最高涨幅','最低价','最低涨幅','收盘价','收盘涨幅','昨收价','涨跌额','涨跌幅(未复权)','成交量 （手）','成交额(千元)','flag']
            # dfR =df[order]
            # writer = pd.ExcelWriter(savefileName)
            # dfR.to_excel(writer,sheet_name=code)

            # writer.save()
            print("...[%d]finish writing Stock =%s to table stock_day"%(i,code))
    # 3.StoreToDB

    # 4.GetGpFxrq
    # 5.Analysis data 
    def GetGpFxrq(self,Code):
        # http://stockpage.10jqka.com.cn/000600/company/
        getH =RandomHeader()
        headers =getH.GetHeader()
        url ="http://basic.10jqka.com.cn/%s/company.html#stockpage"%Code
        req = urllib2.Request(url, headers = headers)
        content = urllib2.urlopen(req).read()
        # text =content.decode('utf8')
        # print('-------')
        # print(content)
        # print('-------')
        soup = BeautifulSoup(content,features="lxml")
        # html = etree.HTML(content)
        # html_data = html.xpath('.//*[@id="publish"]/div[2]/table/tbody/tr[2]/td[1]')
        # # div_mulus = html.xpath('.//*[@class="mulu"]')
        # print(html_data)
        # print(html)
        # for i in html_data:
        #     print(i.text)
        #获取财务报表的表头
        date =""
        try:
            div0 = soup.find("div",{"class":"m_box company_detail"})
            # div0 = soup.find("div",{"id":"publish"})
            dbrow =div0.findAll("tr")
            
            dbrow_cnt =len(dbrow)
            
            if(dbrow_cnt>1):
                date =dbrow[1].findAll("td")[0].contents[1].text
        except Exception as e:
            pass
        return date
        # for k in range(dbrow_cnt):
        #     print(dbrow[k])

      
        # pass


if __name__ == '__main__':
    # https://github.com/sadjjk/tonghuashun_industry
    # https://www.jianshu.com/p/13381aac9245
    test =dataOper("stockA.db")
    # test.GetStockListFromSina()
    # test.GetGpFxrq("300722")
    test.getStockDataInDifferentFileUser('','')


# http://basic.10jqka.com.cn/000600/company.html#stockpage

