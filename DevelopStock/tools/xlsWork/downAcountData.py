#coding=utf-8
import getopt
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
# import csv
# import scipy
# import re
import urllib.request as urllib2
# import xlwt
from bs4 import BeautifulSoup 
# from html.parser import HTMLParser  
# from urllib import request
# from urllib import parse
# from urllib.request import urlopen
import json
import random
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
class AccountPd:
    '''
    获取财务数据 to csv
    pandas 
    '''
    def __init__(self,destPath=".\\Account\\"):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""

        # self.wb = xlwt.Workbook()                            #生成xls表
        # self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        # self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        # self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
        # self.sheet =self.wsZcfzb
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            print("current path=%s"%(os.getcwd()))
            print("%s exist"%(self.destPath))
            pass
        else:
            os.mkdir(destPath)
            print("current path=%s"%(os.getcwd()))
            print("create %s"%(self.destPath))

    def GetFullAcount(self,Code,Name,typeQ ='year'):
        '''
        按年度或者报告季读取报表
        code：股票代码
        name: 股票名称
        typeQ: year -按年度读取 ,其他 按报告季节
        '''
        # self.sheet = self.wsZcfzb
        #资产负债表
        if typeQ=='year':
            nType ='?type=year'
        else:
            nType=''
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html%s'%(nType) #资产负债表
        zcfzb =self.GetZcfzb(Url1,Code)
       

        # self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html%s'%(nType) #利润表
        lrb =self.GetZcfzb(Url1,Code)

        # self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html%s'%(nType) #现金流量表
        llb =self.GetZcfzb(Url1,Code)
        # Name =Name.replace('*', '')
        # if len(self.filename)<=0:
        #     self.wb.save(self.destPath+Name+'('+Code+').csv')
        # else:
        #     self.wb.save(self.destPath+self.filename+'_'+Name+'('+Code+').csv')
        
        # zcfzb.to_excel("%s\%s(%s_%s_zcfzb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # lrb.to_excel("%s\%s(%s_%s_lrb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # llb.to_excel("%s\%s(%s_%s_llb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        zcfzb.to_csv("%s\%s(%s_%s_zcfzb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        lrb.to_csv("%s\%s(%s_%s_lrb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        llb.to_csv("%s\%s(%s_%s_llb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
 
    def GetZcfzb(self,url,code):
        '''
        url - 读取链接
        code -股票代码
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j =0
        df = pd.DataFrame()
        data0 =[]
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td") 
            k =len(cells)
            if k<=0:
                cells =row.findAll("th")
                
                # self.sheet.write(j, 0, cells[0].text)
                data0.append(cells[0].text)
                continue
            # self.sheet.write(j, 0, cells[0].text)  
            data0.append(cells[0].text)   
        # df =df.append(data0)   
        # print(df) 
        #获取财务报表的数据
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})
        df1 = pd.DataFrame()
        col_row=[]
        
        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            data_row =[]
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    # self.sheet.write(j, i+1, cells[i].text)
                    data_row.append(cells[i].text)                                        
                    i=i+1
                # df1 =df1.append(data1)
                if(len(data_row)>1):    
                    data1=dict(zip(col_row,data_row))
                    pds =pd.Series(data1,name =data0[j-1])
                    df1 =df1.append(pds)   
            else:
                cells = row.findAll("th")
                i=0
                while i<len(cells):
                    # self.sheet.write(j,i+1,cells[i].text)
                    col_row.append(cells[i].text)  
                    i=i+1

        zcfzb = df1.T
        # zcfzb.set_index('报告日期', inplace=True)
        zcfzb=zcfzb.sort_index()
        cols =zcfzb.columns.values.tolist()
        for col in cols:
            zcfzb[col] = zcfzb[col].str.replace(',','')
            zcfzb[col] = zcfzb[col].str.replace('--','0')
        zcfzb =zcfzb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        zcfzb.fillna(0,inplace=True)
        return zcfzb

    def Get10jqkaAccount(self,Code,Name,typeQ ='year'):
        '''
        同花顺获取数据
        http://basic.10jqka.com.cn/api/stock/finance/' + $("#stockCode").val() + '_' + reportType + '.json',
        '''
        url_10jqka_base ="http://basic.10jqka.com.cn/api/stock/finance/"
        df_all =pd.DataFrame()
        #资产负债表
        url_zcfzb =url_10jqka_base+"%s_debt.json"%Code
        zcfzb =self.Get10jqkaAccountBase(url_zcfzb,typeQ)
        df_all =df_all.append(zcfzb)
        #利润表
        url_lrb =url_10jqka_base+"%s_benefit.json"%Code
        lrb =self.Get10jqkaAccountBase(url_lrb,typeQ)
        df_all =df_all.append(lrb)
        #现金流量表
        url_llb =url_10jqka_base+"%s_cash.json"%Code
        llb =self.Get10jqkaAccountBase(url_llb,typeQ)
        df_all =df_all.append(llb)
        # 
        # zcfzb.to_csv("%s\%s(%s_%s_zcfzb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        # lrb.to_csv("%s\%s(%s_%s_lrb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        # llb.to_csv("%s\%s(%s_%s_llb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        df_all.to_csv("%s\%s(%s_%s_all).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
    def Get10jqkaAccountBase(self,url,type='year'):
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
        # headers={
        # # 'Referer': 'http://basic.10jqka.com.cn/000002/finance.html',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'        
        # }
        getH =RandomHeader()
        headers =getH.GetHeader()
        # print(headers)
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
        # print(df.T)
        return df
    def GetCodeList(self):
        try:
            print("------开始读取股票基本信息.....")
            ddf =ts.get_stock_basics()
            ddf =ddf.sort_index()

            ddf.to_csv('%s\StockClass.csv'%(self.destPath),encoding='utf_8_sig')
            print("------结束读取股票基本信息.....")
        except Exception as ex:
            print("------读取股票失败.....")
            pass

def main():
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2]) 

    destPath ="%s\\Account"%(sys.argv[1]) 
    xlsTest =AccountPd(destPath=destPath)
    code =sys.argv[2]

    if(code=='stock'):
        xlsTest.GetCodeList()
    else:
        print(sys.argv[3]) 
        name =sys.argv[3]
        # xlsTest.GetFullAcount(code,name,typeQ='year')
        # xlsTest.GetFullAcount(code,name,typeQ='quarter')
        xlsTest.Get10jqkaAccount(code,name,typeQ='year')
        xlsTest.Get10jqkaAccount(code,name,typeQ='quarter')
if __name__ == '__main__':
    main()
    # xlsTest =AccountPd()
    # xlsTest.Get10jqkaAccount('000651','test',typeQ='year')
    # xlsTest.Get10jqkaAccount('000651','test',typeQ='quarter')

