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
from html.parser import HTMLParser  
from urllib import request
from urllib import parse
from urllib.request import urlopen
#####
class Stock:
    def __init__(self,line):
        # 20011231,每股净资产,1.5727,每股收益,0.3438,每股现金含量,11,每股资本公积金,0.5289,
        # 固定资产合计,11,流动资产合计,11,资产总计,11,长期负债合计,16,主营业务收入,11,11,净利润,11
        arr = line.split(",")
        self.day = arr[0].replace("-","") if arr[0]!='-' else '0'
        self.mgzjc = arr[2] if arr[2]!='-' else '0'
        self.mgsy = arr[4] if arr[4]!='-' else '0'
        self.mgxjhl = arr[6] if arr[6]!='-' else '0'
        self.mgjbgjj = arr[8] if arr[8]!='-' else '0'
        self.gdzchj = arr[10] if arr[10]!='-' else '0'
        self.ldzchj = arr[12] if arr[12]!='-' else '0'
        self.zchj = arr[14] if arr[14]!='-' else '0'
        self.cqfzhj = arr[16] if arr[16]!='-' else '0'
        self.zyywsr = arr[18] if arr[18]!='-' else '0'
        self.cwfy = arr[19] if arr[19]!='-' else '0'
        self.jlr = arr[21] if arr[21]!='-' else '0'
        self.series =pd.Series({'日期':self.day,'每股净资产':self.mgzjc,'每股收益':self.mgsy,'每股现金含量':self.mgxjhl,'每股资本公积金':self.mgjbgjj,'固定资产合计':self.gdzchj,
                     '流动资产合计':self.ldzchj,'资产总计':self.zchj,'长期负债合计':self.cqfzhj,'主营业务收入':self.zyywsr,'财务费用':self.cwfy,'净利润':self.jlr})
    def getSeries(self):
        return self.series    


    def __repr__(self):
        # return """day:%s,mgzjc:%s,mgsy:%s,mgxjhl:%s,mgjbgjj:%s,gdzchj:%s,ldzchj:%s,zchj:%s,
        # cqfzhj:%s,zyywsr:%s,cwfy:%s,jlr:%s"""%(self.day,self.mgzjc,self.mgsy,self.mgxjhl,
        #                                        self.mgjbgjj,self.gdzchj,self.ldzchj,self.zchj,
        #                                        self.cqfzhj,self.zyywsr,self.cwfy,self.jlr)
        return """日期:%s,每股净资产:%s,每股收益:%s,每股现金含量:%s,每股资本公积金:%s,固定资产合计:%s,流动资产合计:%s,资产总计:%s,
        长期负债合计:%s,主营业务收入:%s,财务费用:%s,净利润:%s"""%(self.day,self.mgzjc,self.mgsy,self.mgxjhl,
                                               self.mgjbgjj,self.gdzchj,self.ldzchj,self.zchj,
                                               self.cqfzhj,self.zyywsr,self.cwfy,self.jlr)        

class stock_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.handledtags = ['td']
        self.processing = None
        self.data = []

    def handle_starttag(self,tag,attrs):
        if tag in self.handledtags and len(attrs)>0 and attrs[0][0]=='align':
            self.processing = tag

    def handle_data(self,data):
        if self.processing:
            self.data.append(data)

    def handle_endtag(self,tag):
        if tag == self.processing:
            self.processing = None
##### 
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
    def parse_data(self,urldata):
        tp = stock_parser()
        tp.feed(urldata)
        data = tp.data
        i = 0
        arr = []
        stocks = []
        for row in data:
            arr.append(row.replace(",","").replace("元","").replace("\r\n",""))
            i += 1
            if i%22 ==0 and i>0:
                line = ",".join(arr)
                stock = Stock(line)
                stocks.append(stock)
                arr = []
        return stocks


    def get_stock(self,stock_code):
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        url="http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c"%({'stock_code':stock_code})
        req = request.Request(url=url,headers=headers)
        data = str(urlopen(req).read().decode('GBK'))
        data = data.replace("&nbsp;", "-")
        stock = self.parse_data(data)
        return stock
    def getStockBaseAccount(self,code,fileName):
        stocks = self.get_stock(code)
        ret =[]
        for stock in stocks:
            ret.append(stock.getSeries())
        df =pd.DataFrame(ret)
        df.set_index(['日期'],inplace=True)
        df1 =df.T
        df1.to_excel(fileName)        
#主函数 

if __name__ == '__main__':
    Test =CollectFrom163()    
    # Test.Set_Stock_fName("test") 
    # Test.Set_Stock_Item("3")
    # Test.Set_Stock_Text("现金及现金等价物净增加额(万元)")
    # kk = ts.get_industry_classified()
    # print(kk)
    # # df = Test.Get_Stock_List()
    # # count = 1
    # # Test.GetFullAcount('601319')n
    # Test.get_industry_classified('家电行业',1)


    # stocks = Test.get_stock("002122")
    Test.getStockBaseAccount("000651",'test.xls')
    # ret =[]
    # for stock in stocks:
    #     print (stock)
    #     ret.append(stock.getSeries())
    # df =pd.DataFrame(ret)
    # df.set_index(['日期'],inplace=True)
    # print(df)
    # df1 =df.T
   
    # df1.to_excel('test.xls')