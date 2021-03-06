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
    获取分红 和 最新 股票列表
    '''
    def __init__(self,destPath=".\\Account\\"):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""

        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            print("current path=%s"%(os.getcwd()))
            print("%s exist"%(self.destPath))
            pass
        else:
            os.mkdir(destPath)
            print("current path=%s"%(os.getcwd()))
            print("create %s"%(self.destPath)) 

    def GetFhpg_CSV(self,Code,Name):
        '''
        file format
        .csv
        '''
        try:
            Url1 = 'http://quotes.money.163.com/f10/fhpg_%s.html'%Code
            fhpg =self.GetFhpgBase(Url1,Code)
            if(len(fhpg)>=0):
                columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
                fhpg.to_csv("%s\%s(%s_fhpg).csv"%(self.destPath,Code,Name),index_label=u'序号',columns =columns,encoding='utf_8_sig')
            else:
                print("%s(%s) 分红数据不存在"%(Code,Name))
        except Exception as ex:
            print("%s(%s) 分红数据读取异常"%(Code,Name))

    def GetFhpg(self,Code,Name):
        '''
        file format
        .xls
        '''
        try:
            
            Url1 = 'http://quotes.money.163.com/f10/fhpg_%s.html'%Code
            outFile ="%s\%s(%s_fhpg).xls"%(self.destPath,Code,Name)
            write = pd.ExcelWriter(outFile)
            fhpg =self.GetFhpgBase(Url1,Code)
            if(len(fhpg)>=0):
                columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
                fhpg =fhpg[columns]
                fhpg.to_excel(write,sheet_name='历史分红',index=False)
                write.save() 
            else:
                print("          %s(%s) 分红数据不存在"%(Code,Name))
        except Exception as ex:
            print("           %s(%s) 分红数据读取异常[%s]"%(Code,Name,ex))


    def GetFhpgBase(self,url,code):
        '''
        get FHPG 分红配股
        '''
        getH =RandomHeader()
        headers =getH.GetHeader()
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        dbrow =table0.findAll("tr")
       
        df1 = pd.DataFrame()
       
        dbrow_cnt =len(dbrow)
        col_row =[]
        for k in range(dbrow_cnt):
            if(k<2):
                cells =dbrow[k].findAll("th")
                for cells_col in range(len(cells)):
                    col_name = cells[cells_col].text
                    if(col_name =="分红方案（每10股）"):
                        col_row.append("")
                        col_row.append("")
                        col_row.append("")
                        pass
                    else:
                        if(k==1):
                           col_row[cells_col+2] = col_name
                        else:
                            col_row.append(col_name)
            else:
                cells =dbrow[k].findAll("td")
                data_row =[]
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < lencell:

                        data_row.append(cells[i].text)                                        
                        i=i+1
                    if(len(data_row)>1):    
                        data1=dict(zip(col_row,data_row))
                        row_name ='%d'%(k-2)
                        pds =pd.Series(data1,name =row_name)
                        df1 =df1.append(pds)                   
        data_fh = df1

        # data_fh=data_fh.sort_index()
        # cols =data_fh.columns.values.tolist()
        # for col in cols:
        #     data_fh[col] = data_fh[col].str.replace(',','')
        #     data_fh[col] = data_fh[col].str.replace('--','0')
        # data_fh =data_fh.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        # data_fh.fillna(0,inplace=True)
        return data_fh
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
        # 
    def GetStockListFromNet(self):
        print("------开始读取网上股票列表信息")
        self.df = ts.get_stock_basics()             
        self.df =self.df.sort_values(by=['code'])
        write = pd.ExcelWriter('stockListAccount.xls')     #存储到文件  stockList.xls  
        self.df.to_excel(write,index=True)
        write.save()
        print("------结束读取网上股票列表信息")
        # 
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
            # time.sleep(random.uniform(1.1,3.4) )
            time.sleep(random.random()+1)
        write = pd.ExcelWriter('stockListAccount.xls')
        # columns =['symbol','code','name','open','high','low','buy','amount','changepercent','mktcap','nmc','pb','per','pricechange','sell','settlement','trade','turnoverratio','volume','ticktime']
        columns =['code','name']
        df.to_excel(write,index=True,columns=columns)
        write.save()
        print("------结束读取网上股票列表信息")    
       
    def jsonfy(self,s):
        #此函数将不带双引号的json的key标准化
        obj = eval(s, type('js', (dict,), dict(__getitem__=lambda s, n: n))())
        return obj

    def GetAccountDataFromSina(self,code,table_type):
        '''
        all data
        table_type :"zcfzb","lrb","llb"
        '''
        has_data = True
        #获取当前年份
        today = pd.to_datetime(time.strftime("%x"))
        year = today.year    #数据用pandas的dataframe储存
        dataArr = pd.DataFrame() 
        time.sleep(random.random()+1) 
        while has_data: 
            
            try:
                dataArr =self.GetAccountDataFromSinaBase(code,year,dataArr,table_type)
                year -=1
            except:
                if (year+1)==today.year:
                    has_data=True
                else:
                    has_data=False
        dataArr = dataArr.T
        dataArr =dataArr.dropna(axis=0,thresh=10) 
        dataArr =dataArr.dropna(axis=1,thresh=10) 
        try:
            dataArr = dataArr.set_index(dataArr.columns[0])
        except:
            dataArr=dataArr
        return dataArr

    def GetAccountData_ALL(self,code):
        write = pd.ExcelWriter(code +"_zcfzb.xlsx")
        zcfzb =self.GetAccountDataFromSina(code,'zcfzb')
        zcfzb.to_excel(write,sheet_name='zcfzb',index=True)
        

        lrb =self.GetAccountDataFromSina(code,'lrb')
        lrb.to_excel(write,sheet_name='lrb',index=True)

        llb =self.GetAccountDataFromSina(code,'llb')
        llb.to_excel(write,sheet_name='llb',index=True)
        write.save()

    def GetAccountDataFromSinaOne(self,code,year,table_type='zcfzb'):
        '''
        get one year data
        table_type :"zcfzb","lrb","llb"
        '''
        dataArr =pd.DataFrame()
        try:
            dataArr =self.GetAccountDataFromSinaBase(code,year,dataArr,table_type)
            dataArr = dataArr.T
            dataArr =dataArr.dropna(axis=0,thresh=10) 
            dataArr =dataArr.dropna(axis=1,thresh=10) 
            try:
                dataArr = dataArr.set_index(dataArr.columns[0])
            except:
                dataArr=dataArr
        except:
            pass
        return dataArr

    def GetAccountDataFromSinaBase(self,code,year,dataArr,table_type='zcfzb'):
        '''
        table_type :"zcfzb","lrb","llb","fhpg"
        Bbase function for getting account data from sina
        add try catch block to avoid exception.
        http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600519/ctrl/part/displaytype/4.phtml
        http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/600519/ctrl/2019/displaytype/4.phtml
        '''  
        if(table_type==''):
            table_type ='zcfzb'
            Id ="BalanceSheetNewTable0" 
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        # zcfzb id="BalanceSheetNewTable0" 
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
        # lrb id="ProfitStatementNewTable0"
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/4.phtml'
        # llb id="ProfitStatementNewTable0"
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/4.phtml'
        if (table_type =='zcfzb'):
            Id ="BalanceSheetNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if(table_type =='lrb'):
            Id="ProfitStatementNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if(table_type =='llb'):
            Id="ProfitStatementNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if(table_type=='fhpg'):
            Id="sharebonus_1"
            FINIANCE_SINA_URL ='http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'
            furl = FINIANCE_SINA_URL%(code)        #获取数据，标准处理方法
        getH =RandomHeader()
        headers =getH.GetHeader()
        request = urllib2.Request(furl, headers = headers)
        text = urllib2.urlopen(request, timeout=5).read()
        text = text.decode('gbk')
        html = lxml.html.parse(StringIO(text))        #分离目标数据
        # res = html.xpath("//table[@id=\"BalanceSheetNewTable0\"]")#ProfitStatementNewTable0

        res = html.xpath(("//table[@id=\"%s\"]")%Id)
        sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
        sarr = ''.join(sarr)
        sarr = '<table>%s</table>'%sarr        #向前滚动一年
        # year-=1
        #对最后一页进行判断，依据是数据是否有
                   #将数据读入到dataframe数据个数中；并进行连接；
        
        df = read_html(sarr)[0]
        df.columns=range(0,df.shape[1])
        df = df.set_index(df.columns[0])
        dataArr = [dataArr, df]
        # dataArr = pd.concat(dataArr, axis=1, join='inner')
        dataArr = pd.concat(dataArr, axis=1)
        return dataArr

    def GetAccountData_ALL_XLS(self,Code,Name):
        self.wb = xlwt.Workbook()                            #生成xls表
        self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
         #资产负债表
        self.sheet =self.wsZcfzb
        self.GetAccountDataFromSinaXls(Code,'zcfzb')
        
        #利润表
        self.sheet = self.wsLrb
        self.GetAccountDataFromSinaXls(Code,'lrb')
        
        #现金流量表
        self.sheet = self.wsXjllb
        self.GetAccountDataFromSinaXls(Code,'llb')
        Name =Name.replace('*', '')
        self.wb.save(self.destPath+Code+'('+Name+').xls')

    def GetAccountDataFromSinaXls(self,code,table_type):
        has_data = True
        #获取当前年份
        today = pd.to_datetime(time.strftime("%x"))
        year = today.year    #数据用pandas的dataframe储存
        hasHead_col =0
        time.sleep(random.random()+1) 
        while has_data: 
            
            try:
                hasHead_col =self.GetAccountDataFromSinaBaseXls(code,year,hasHead_col,table_type)
                year -=1
            except:
                if (year+1)==today.year:
                    has_data=True
                else:
                    has_data=False
           
    def GetAccountDataFromSinaYearXls(self,code,name,year):
        '''
        按照年份提取报表数据
        '''
        self.wb = xlwt.Workbook()                            #生成xls表
        self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
         #资产负债表
        self.sheet =self.wsZcfzb
        self.GetAccountDataFromSinaBaseXls(code,year,0,'zcfzb')

        #利润表
        self.sheet = self.wsLrb
        self.GetAccountDataFromSinaBaseXls(code,year,0,'lrb')
        #现金流量表
        self.sheet = self.wsXjllb        
        self.GetAccountDataFromSinaBaseXls(code,year,0,'llb')
        name =name.replace('*', '')
        self.wb.save(self.destPath+code+'('+name+'_'+year+').xls')

    def GetAccountDataFromSinaBaseXls(self,code,year,hasHead_col,table_type='zcfzb'):
        '''
        hasHead_col is max number of columns
        # zcfzb id="BalanceSheetNewTable0" 
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
        # lrb id="ProfitStatementNewTable0"
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/4.phtml'
        # llb id="ProfitStatementNewTable0"
        # FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/4.phtml'

        '''
        if(table_type==''):
            table_type ='zcfzb'
            Id ="BalanceSheetNewTable0" 
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if (table_type =='zcfzb'):
            Id ="BalanceSheetNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if(table_type =='lrb'):
            Id="ProfitStatementNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        if(table_type =='llb'):
            Id="ProfitStatementNewTable0"
            FINIANCE_SINA_URL = 'http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/%s/ctrl/%s/displaytype/4.phtml'
            furl = FINIANCE_SINA_URL%(code,year)        #获取数据，标准处理方法
        getH =RandomHeader()
        headers =getH.GetHeader()        
        req = urllib2.Request(furl, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"id":Id})
        j=0
        for row in table0.findAll("tr"):
            cells = row.findAll("td")
            k =len(cells)
            if(k <=0):
                continue
            else:
                j+=1
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    if(hasHead_col>0):
                        if (i>0):
                            self.sheet.write(j, hasHead_col + i , cells[i].text)
                    else:
                        self.sheet.write(j, i , cells[i].text)                                        
                    i=i+1  
        if(i>0):
            i= i-1  
        return i + hasHead_col          



    def RegularData(self,code,data,type_table):
        '''
        序号	股票代号	报告日期	报表名称	科目名称	数值

        '''
        col_count = data.shape(1)
        row_count = data.shape(0)
        
        rowData =[]
        for k in range(row_count):
            for j in range(col_count):
                rowData.append(['',code,data[k][0],type_table,data.columns[j],data[k][j]])
        df =pd.DataFrame(rowData,['序号','股票代号','报告日期',	'报表名称','科目名称','数值'])
        return df
                

    def GetFhpgSina(self,code,name):
        '''
        get fen hong and pei gu
        http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/600519.phtml
        '''
        dataArr =pd.DataFrame()
        try:
            Id="sharebonus_1"
            FINIANCE_SINA_URL ='http://money.finance.sina.com.cn/corp/go.php/vISSUE_ShareBonus/stockid/%s.phtml'
            furl = FINIANCE_SINA_URL%(code)        #获取数据，标准处理方法
            getH =RandomHeader()
            headers =getH.GetHeader()
            request = urllib2.Request(furl, headers = headers)
            text = urllib2.urlopen(request, timeout=5).read()
            text = text.decode('gbk')
            html = lxml.html.parse(StringIO(text))        #分离目标数据
            # res = html.xpath("//table[@id=\"BalanceSheetNewTable0\"]")#ProfitStatementNewTable0

            res = html.xpath(("//table[@id=\"%s\"]")%Id)
            sarr = [etree.tostring(node).decode('gbk') for node in res]        #存储文件
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr        #向前滚动一年
            # year-=1
            #对最后一页进行判断，依据是数据是否有
                    #将数据读入到dataframe数据个数中；并进行连接；
            
            df = read_html(sarr)[0]
            # df.columns=range(0,df.shape[1])
            # df = df.set_index(df.columns[0])
            dataArr = [dataArr, df]
            # dataArr = pd.concat(dataArr, axis=1, join='inner')
            dataArr = pd.concat(dataArr, axis=1)
            columns =[]
            cnt =len(dataArr.columns.levels[2])
            for k in range(cnt):
                columns.append(dataArr.columns.levels[2][dataArr.columns.codes[2][k]])
            dataArr.columns =columns
            dataArr =dataArr.drop(['查看详细'],axis=1)
            
            outFile ="%s\%s(%s_fhpg).xls"%(self.destPath,code,name)
            write = pd.ExcelWriter(outFile)

            if(len(dataArr)>=0):
                # columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
                # '公告日期'	'送股(股)'	'转增(股)'	'派息(税前)(元)'	'进度'	'除权除息日'	'股权登记日'	'红股上市日'
                # 序号	股票代号	公告年度	公告日期	分红年度	送股	转增	派息	股权登记日	除权除息日	红股上市日

                # dataArr =dataArr[columns]
                dataArr.to_excel(write,sheet_name='历史分红',index=False)
                write.save() 
            else:
                print("          %s(%s) 分红数据不存在"%(code,name))
     
        except Exception as ex:
             print("           %s(%s) 分红数据读取异常[%s]"%(code,name,ex))
        return dataArr
    def web_access_delay(self):
        time.sleep(random.random()+1) 
def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'a:h',['all=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()
    all =""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("")
            print("-----命令格式，参照例子:-----------------------------------------------")
            print("|         获取股票列表:")
            print("|                 python ForJerryTaobao.py -a stock")
            print("|         获取所有股票的分红数据:")
            print("|                 python ForJerryTaobao.py -a fh")
            print("|         获取指定股票的分红数据:")
            print("|                 python ForJerryTaobao.py fh 000651 格力电器")
            print("|         获取所有股票的财务数据:")
            print("|                 python ForJerryTaobao.py -a cw")
            print("|         获取指定股票的财务数据:")
            print("|                 python ForJerryTaobao.py cw 000651 格力电器")
            print("|         获取指定股票的财务数据 按年提取:")
            print("|                 python ForJerryTaobao.py cw 000651 格力电器 2018")
            print("---------------------------------------------------------------------")
            sys.exit()
        elif o in ("-a", "--all"): #所有股票读取
            all = a
    
    if(all =='fh'):

        xlsTest =AccountPd()
        retDf =xlsTest.GetCodeList()
        time_start_total=time.time()
        k=0
        for code in retDf.index:
            # code =retDf.loc[k,'code']
            name = retDf.loc[code,'name'] 
            name =name.replace('*','')
            
            index_k ='序号:%04d'%k
            k =k +1
            print("[%s]开始读取分红数据 %s(%s)"%(index_k,code,name))
            time_start=time.time()
            xlsTest.GetFhpgSina(code,name)                          #分红
            time_end=time.time()
            time_escape =time_end -time_start
            time.sleep(random.random()+1)
            print("[%s,耗时%s(s)]结束读取分红数据 %s(%s)"%(index_k,time_escape,code,name))
            
        time_end_total=time.time()  
        time_escape_total = time_end_total - time_start_total
        print("共计 耗时%s(s)"%(time_escape_total))  
    elif(all =='cw'): 
        xlsTest =AccountPd()
        retDf =xlsTest.GetCodeList()
        time_start_total=time.time()
        k=0
        for code in retDf.index:
            name = retDf.loc[code,'name'] 
            name =name.replace('*','')
            index_k ='序号:%04d'%k
            k =k +1
            print("[%s]开始读取财务数据 %s(%s)"%(index_k,code,name))
            time_start=time.time()
            xlsTest.GetAccountData_ALL_XLS(code,name)  
            time_end=time.time()
            time_escape =time_end -time_start
            time.sleep(random.random()+1)
            print("[%s,耗时%s(s)]结束读取财务数据 %s(%s)"%(index_k,time_escape,code,name))
        time_end_total=time.time()  
        time_escape_total = time_end_total - time_start_total
        print("共计 耗时%s(s)"%(time_escape_total))   
    elif (all =='stock'):
        xlsTest =AccountPd()
        # xlsTest.GetStockListFromNet()
        xlsTest.GetStockListFromSina()
    else:
        typeW = sys.argv[1]
        if(typeW =='fh'):
            
            code =sys.argv[2]
            xlsTest =AccountPd()
            name =sys.argv[3]
            name =name.replace('*','')
            print("----开始读取 %s(%s)"%(code,name))
            time_start_total=time.time()
            xlsTest.GetFhpg(code,name)                          #分红
            time_end_total=time.time()  
            time_escape_total = time_end_total - time_start_total
            print("----结束读取 %s(%s),耗时%s(s)"%(code,name,time_escape_total)) 
        elif(typeW =='cw'):
            code =sys.argv[2]
            xlsTest =AccountPd()
            name =sys.argv[3]
            name =name.replace('*','')

            time_start_total=time.time()
            if(len(sys.argv)>4):
                year =sys.argv[4]
                time_start_total=time.time()
                print("----开始读取 %s(%s %s)"%(code,name,year))
                xlsTest.GetAccountDataFromSinaYearXls(code,name,year)
            else:
                time_start_total=time.time()
                print("----开始读取 %s(%s)"%(code,name))
                xlsTest.GetAccountData_ALL_XLS(code,name)                    #财务报表
            time_end_total=time.time()  
            time_escape_total = time_end_total - time_start_total

            print("----结束读取 %s(%s),耗时%s(s)"%(code,name,time_escape_total)) 

if __name__ == '__main__':
    # only for python command - MainOpt()
    MainOpt()

    # test =AccountPd()
    # # 股票代号
    # # test.GetStockListFromSina()
    # test.web_access_delay()
    # # 资产负债表
    # # test.GetAccountData_ALL('000001')
    # test.GetAccountData_ALL_XLS('000001','test')

    # 利润表
    # 现金流量表


