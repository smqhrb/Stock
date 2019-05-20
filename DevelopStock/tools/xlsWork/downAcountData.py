#coding=utf-8
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

        self.wb = xlwt.Workbook()                            #生成xls表
        self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
        self.sheet =self.wsZcfzb
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            pass
        else:
            os.mkdir(destPath)

    def GetFullAcount(self,Code,Name,type ='year'):
        '''
        按年度或者报告季读取报表
        code：股票代码
        name: 股票名称
        type: year -按年度读取 ,其他 按报告季节
        '''
        self.sheet = self.wsZcfzb
        #资产负债表
        if type=='year':
            nType ='?type=year'
        else:
            nType=''
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html%s'%(nType) #资产负债表
        self.GetZcfzb(Url1,Code)

        self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html%s'%(nType) #利润表
        self.GetZcfzb(Url1,Code)

        self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html%s'%(nType) #现金流量表
        self.GetZcfzb(Url1,Code)
        Name =Name.replace('*', '')
        if len(self.filename)<=0:
            self.wb.save(self.destPath+Name+'('+Code+').csv')
        else:
            self.wb.save(self.destPath+self.filename+'_'+Name+'('+Code+').csv')

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
                
                self.sheet.write(j, 0, cells[0].text)
                data0.append(cells[0].text)
                continue
            self.sheet.write(j, 0, cells[0].text)  
            data0.append(cells[0].text)   
        df =df.append(data0)   
        print(df) 
        #获取财务报表的数据
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})
        df1 = pd.DataFrame()
        col_row=[]
        data_row =[]
        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    self.sheet.write(j, i+1, cells[i].text)
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
                    self.sheet.write(j,i+1,cells[i].text)
                    col_row.append(cells[i].text)  
                   
                    i=i+1

        print(df1)
        return lencell


def test():
    xlsTest =AccountPd()
    xlsTest.GetFullAcount('000651','格力电器')

if __name__ == '__main__':
    test()