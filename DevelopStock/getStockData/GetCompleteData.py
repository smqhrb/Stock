# 本文计划实现对网页财经上的上市公司财务报表中某个特定财务数据的抓取，
# 例如历年的应收票据，全部抓取后存放到excel文件中。


#coding=utf-8
import tushare as ts
#import talib as ta
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import csv
import scipy
import re
import urllib.request as urllib2
import xlwt
from bs4 import BeautifulSoup 

class CollectFrom163:
    def __init__(self):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""

        self.wb = xlwt.Workbook()
        self.wsZcfzb = self.wb.add_sheet(u'资产负债表')
        self.wsLrb = self.wb.add_sheet(u'利润表')
        self.wsXjllb = self.wb.add_sheet(u'现金流量表')
        self.sheet =self.wsZcfzb
        
        

#获取股票列表
#code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
# fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
    def Get_Stock_List(self):
        self.df = ts.get_stock_basics()
        return self.df

    def Set_Stock_Code(self,Code):
        self.code =Code

    def Set_Stock_fName(self,filename):
        self.filename =filename

    def Set_Stock_Item(self,item):
        self.item =item

    def Set_Stock_Text(self,text):
        self.text =text

    def Set_Xls_Sheet(self,sheet):
        self.sheet =sheet


           
# 主要抓取函数在下面，要分析数据在网页上的呈现方式进而选择合适的抓取方式。
# 网易股票的资产负债表的应收票据的数据其实被拆成了2张表，第一张表是纯表头，第二张表是纯数据。

    def GetZcfzb(self,url,code):
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content)
    #所以要在第一张表中先找到应收票据的位置。
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j =0
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td") 
            k =len(cells)
            if k<=0:
                cells =row.findAll("th")
                self.sheet.write(j, 0, cells[0].text)
                continue
            self.sheet.write(j, 0, cells[0].text)          

        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})

        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    #print cells[i].text
                    self.sheet.write(j, i+1, cells[i].text)                                        
                    i=i+1
            else:
                cells = row.findAll("th")
                i=0
                while i<len(cells):
                    self.sheet.write(j,i+1,cells[i].text)
                    i=i+1
        return lencell

#抓取网页数据
    def Get_3_Cell(self,url,code,count,headyear):
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content)

        #所以要在第一张表中先找到应收票据的位置。
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j=-1
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td")            
            if len(cells) > 0:#
                if cells[0].text.find(self.text)>=0:
                    position = j
                    #print position
                    break;
                
    #然后到第二张表中去抓对应位置的数据。
        lencell=0
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})

        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            if headyear ==0:
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < len(cells):
                        #print cells[i].text
                        self.sheet.write(j, i+1, cells[i].text)                                        
                        i=i+1
                    
        j=-1
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            if j == position:       
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < len(cells):
                        #print cells[i].text
                        self.sheet.write(count, i+2, cells[i].text)                                        
                        i=i+1
                break;
        return lencell

    def GetAllFullAcount(self,df_Code):
        for Code in df_Code.index:
            Name = df_Code.loc[Code,'name']
            print(u"股票:"+Name+"(" + Code +")")
            self.wb = xlwt.Workbook()
            self.wsZcfzb = self.wb.add_sheet(u'资产负债表')
            self.wsLrb = self.wb.add_sheet(u'利润表')
            self.wsXjllb = self.wb.add_sheet(u'现金流量表')
            #self.wsZycwzb = self.wb.add_sheet(u'主要财务指标')
            self.sheet =self.wsZcfzb
            self.GetFullAcount(Code,Name)
            
    def GetFullAcountTop(self,df_Code,Code):    
        Name = df_Code.loc[Code,'name']
        print(u"股票:"+Name+"(" + Code +")")
        self.GetFullAcount(Code,Name)        


    def GetFullAcount(self,Code,Name):
        
        self.sheet = self.wsZcfzb
        #资产负债表
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html?type=year'
        self.GetZcfzb(Url1,Code)
        #wb.save('Get3Data1.xls')

        self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html?type=year'
        self.GetZcfzb(Url1,Code)
        #wb.save('Get3Data1.xls')
        self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html?type=year'
        self.GetZcfzb(Url1,Code)
        # self.sheet = self.wsZycwzb
        # Url1 = 'http://quotes.money.163.com/f10/zycwzb_'+Code+'.html?type=year'
        # self.GetZcfzb(Url1,Code)
        if len(self.filename)<=0:
            self.wb.save(Name+'('+Code+').xls')
        else:
            self.wb.save(self.filename+'_'+Name+'('+Code+').xls')
        

    def GetData(self,df_Code,count):
        headyear =1
        if (len(self.item)==0 or self.item =='1'):
            self.sheet = self.wsZcfzb             
        elif self.item =='2':
            self.sheet = self.wsLrb
        elif self.item =='3':
            self.sheet = self.wsXjllb
        elif self.item =='4':
            self.sheet = self.wsZcfzb

        for Code in df_Code.index:
            Name = df_Code.loc[Code,'name']
            print(u"股票:"+Name+"(" + Code +") text="+self.text)
            self.sheet.write(count, 0, Code)
            self.sheet.write(count, 1, Name)   
            if (len(self.item)==0 or self.item =='1'):
                Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html?type=year'  
                prefix ='zcfzb_'   
                            
            elif self.item =='2':
                Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html?type=year'
                prefix ='lrb_' 
               
            elif self.item =='3':
                Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html?type=year'
                prefix ='xjllb_'
                
            elif self.item =='4':
                Url1 = 'http://quotes.money.163.com/f10/zycwzb_'+Code+'.html?type=year'
                prefix ='zycwzb_'                 
            LenCell1 = self.Get_3_Cell(Url1,Code,count,headyear)
            count =count+1
        
        self.wb.save(prefix +Code+'.xls')

    def get_industry_classified(self,classify,count):
        ddf =ts.get_industry_classified()
        ddf1 =ddf.copy()
        a =ddf1[ddf1['c_name'].isin([classify])] 
        headyear =0
        # self.wb = xlwt.Workbook()
        # self.wsZcfzb = self.wb.add_sheet(u'资产负债表')
        # self.wsLrb = self.wb.add_sheet(u'利润表')
        # self.wsXjllb = self.wb.add_sheet(u'现金流量表')
        # self.sheet =self.wsZcfzb      

        if (len(self.item)==0 or self.item =='1'):
            self.sheet = self.wsZcfzb             
        elif self.item =='2':
             self.sheet = self.wsLrb
        elif self.item =='3':
            self.sheet = self.wsXjllb
        elif self.item =='4':
            self.sheet = self.wsZcfzb
        prefix ='NA_' 
        for ind in a.index:
            Code =a.loc[ind,"code"]
            Name =a.loc[ind,"name"]
            print("Stock="+Name+"("+Code+")")

            self.sheet.write(count, 0, Code)
            self.sheet.write(count, 1, Name)        
            if (len(self.item)==0 or self.item =='1'):
                Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html?type=year'  
                prefix ='zcfzb_'                  
            elif self.item =='2':
                Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html?type=year'
                prefix ='lrb_' 
            elif self.item =='3':
                Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html?type=year'
                prefix ='xjllb_'
            elif self.item =='4':
                Url1 = 'http://quotes.money.163.com/f10/zycwzb_'+Code+'.html?type=year'
                prefix ='zycwzb_'
            
            LenCell1 = self.Get_3_Cell(Url1,Code,count,headyear)
            headyear =1
            count =count+1
  
        self.wb.save(prefix+'['+classify+'('+ self.text+')].xls')    
        
        # self.GetData(ddf,0)

#主函数 

if __name__ == '__main__':
    Test =CollectFrom163()    
    Test.Set_Stock_fName("test") 
    Test.Set_Stock_Item("3")
    Test.Set_Stock_Text("现金及现金等价物净增加额(万元)")
    kk = ts.get_industry_classified()
    print(kk)
    # df = Test.Get_Stock_List()
    # count = 1
    # Test.GetFullAcount('601319')n
    Test.get_industry_classified('家电行业',1)