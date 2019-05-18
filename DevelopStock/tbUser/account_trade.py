from openpyxl import load_workbook
import openpyxl
import tushare as ts
import numpy as np
import pandas as pd

import re
import urllib.request as urllib2
import xlwt
from bs4 import BeautifulSoup 
from html.parser import HTMLParser  
from urllib import request
from urllib import parse
from urllib.request import urlopen 
import xlwt
import sys
import os
import time

import tushare as ts
import datetime
from datetime import timedelta
import getopt
import numpy as np
import random
stock_CodeUrl = 'http://quote.eastmoney.com/stocklist.html'
print("Script name：",sys.argv[0])
print("")
len1 =len(sys.argv)

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'f:s:e:h',['files=','start=','end=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()

    files=""

    start =""
    end =""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("---------help content------------------------------------------------------")
            print("|   -f fname          [get all stock data from config file]       ")
            print("|   -s 20170111       [start time,format YYYYMMDD]                       ")
            print("|   -e 20180111       [end   time,format YYYYMMDD]                 ")
            
            print("|   for example:")
            print("|      example 2: all stock data write in different files")
            print("|           python main.py -f stockList.txt -s 20170111 -e 20180111")
            print("|      example 3: default time is now to now -365day")
            print("|           python main.py -f stockList.txt")
            print("|                                           ")
            print("|   stock code is 601800.SH or 300298.SZ or 000882.SZ")
            print("---------------------------------------------------------------------------------")
            sys.exit()
        elif o in ("-f", "--files"):
            files = a

        elif o in ("-s","--start"):
            start =a
        elif o in ("-e","--end"):
            end =a

        else:
            sys.exit()

    print("Please confirm xls file not to be covered in current folder")
    print("Continue? Please input 'y' to continune,'n' to end this program.")
    str = input("Enter your input: ")
    if str=='n':
        exit()
    elif str=='y':
        pass
    # files="stockList.txt"
    if len(files)>0:
        print("configure file name ="+files)
        if len(start)==0 and len(end)==0:
            now_time = datetime.datetime.now()
            # end =now_time.strftime('%Y-%m-%d')
            # lastyear_time =now_time -timedelta(days=365)
            # start =lastyear_time.strftime('%Y-%m-%d')
            end =now_time.strftime('%Y%m%d')
            lastyear_time =now_time -timedelta(days=365)
            start =lastyear_time.strftime('%Y%m%d')

        print("Start time ="+start)
        print("End time   ="+end)
        stockCodeList =readStockList(files)
        print("...start to read data...")
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')

        getStockDataInDifferentFile(stockCodeList,start,end)
        print("...end.................")
    else:
        print("...without stock code ,program end....")
        exit()


#获取股票代码列表
def urlTolist(url):
    allCodeList = []
    html = urllib2.urlopen(url).read()
    html = html.decode('utf-8')
    print(html)
    # html = str(urlopen(url).read().decode('gb2312'))
    # s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    # s = r'<td class=" listview-col-Code"><a href="/sz300256.html">'
    s = r'<td class=" listview-col-Code"><a href="/(.*).html">'
    # <td class=" listview-col-Code"><a href="/sz300256.html">300256</a></td>
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        if item[0]=='6' or item[0]=='3' or item[0]=='0':
            allCodeList.append(item)
    return allCodeList

def readStockList(fname):
    contents =[]
    f = open(fname)
    lines = f.readlines()
    for code in lines:
        k =code.strip()
        if(k=='all'):
            # pro = ts.pro_api()
            # data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            # contents =data['ts_code'].tolist()
            
            df=pd.read_csv('stockList.csv',header=None,encoding = "gbk")
            print(df[0])
            df[0] =df[0].astype(int)
            contents =df[0].tolist()
            # contents =urlTolist(stock_CodeUrl)
            for i in range(len(contents)):
                contents[i] ="%06d"%contents[i]
                if(contents[i]>'600000'):
                    contents[i]=contents[i]+'.SH'
                else:
                    contents[i]=contents[i]+'.SZ'
            break
        else:
            
            if len(k)>0:
                contents.append(k)
    f.close()
    print("....Stock Code List............")
    print(contents)
    return contents

# def getStockDataInDifferentFile(stockCodeList,start,end):
#     '''
#     tushare
#     '''
#     path ="./%sTo%s"%(start,end)
#     if(os.path.exists(path)==False): #判断目标是否存在 
#         os.mkdir(path) #创建目录
#     pro = ts.pro_api()
#     i=0
#     for code in stockCodeList:
#         savefileName =path+'/'+code+'('+start+'To'+end+').xlsx'
#         i =i+1
#         if(os.path.exists(savefileName)):
#             print("...[%d]%s exist"%(i,savefileName))
#             continue
#         time.sleep(0.3)
#         print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
#         # df =ts.get_hist_data(code,start=start,end=end)
#         # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

#         df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
   
#         df=df1.sort_values(by=['trade_date'])
 
#         writer = pd.ExcelWriter(savefileName)
#         df.to_excel(writer,sheet_name="交易价格")
        
#         jbxx =getStockBaseAccount(code[:-3])
#         if(len(jbxx)>0):
#             jbxx['主营业务收入'] = jbxx['主营业务收入'].astype(float)
#             jbxx['净利润'] = jbxx['净利润'].astype(float)
#             jbxx['固定资产合计'] = jbxx['固定资产合计'].astype(float)
#             jbxx['每股净资产'] = jbxx['每股净资产'].astype(float)
#             jbxx['每股现金含量'] = jbxx['每股现金含量'].astype(float)
#             jbxx['每股资本公积金'] = jbxx['每股资本公积金'].astype(float)
#             jbxx['流动资产合计'] = jbxx['流动资产合计'].astype(float)
#             jbxx['财务费用'] = jbxx['财务费用'].astype(float)
#             jbxx['资产总计'] = jbxx['资产总计'].astype(float)
#             jbxx['长期负债合计'] = jbxx['长期负债合计'].astype(float)
#             jbxx['每股收益'] = jbxx['每股收益'].astype(float)
#         jbxx.to_excel(writer,sheet_name='基本指标(元)',index=True)
#         writer.save()
#         print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))

def getStockDataInDifferentFile(stockCodeList,start,end):
    '''
    #     test =tradeData()
#     test.getDataDayUse("AAAA.xls","000651","2018-03-01","2019-04-28",'1')
    '''
    path ="./%sTo%s"%(start,end)
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    # pro = ts.pro_api()
    test =tradeData()
    i=0
    for code in stockCodeList:
        time_start=time.time()

        savefileName =path+'/'+code+'('+start+'To'+end+').xlsx'
        i =i+1
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            continue 
        delayt =2*random.random()+1
        time.sleep(delayt)
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

        # df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
   
        # df=df1.sort_values(by=['trade_date'])
        startDate =datetime.datetime.strptime(start, "%Y%m%d")
        strStart =startDate.strftime("%Y-%m-%d")
        endDate = datetime.datetime.strptime(end, "%Y%m%d")
        strEnd =endDate.strftime("%Y-%m-%d")
        df =test.getDataDayUse("AAAA.xls",code[:-3],strStart,strEnd,'1')
 
        writer = pd.ExcelWriter(savefileName)
        df.to_excel(writer,sheet_name="交易价格")
        
        jbxx =getStockBaseAccount(code[:-3])
        if(len(jbxx)>0):
            jbxx['主营业务收入'] = jbxx['主营业务收入'].astype(float)
            jbxx['净利润'] = jbxx['净利润'].astype(float)
            jbxx['固定资产合计'] = jbxx['固定资产合计'].astype(float)
            jbxx['每股净资产'] = jbxx['每股净资产'].astype(float)
            jbxx['每股现金含量'] = jbxx['每股现金含量'].astype(float)
            jbxx['每股资本公积金'] = jbxx['每股资本公积金'].astype(float)
            jbxx['流动资产合计'] = jbxx['流动资产合计'].astype(float)
            jbxx['财务费用'] = jbxx['财务费用'].astype(float)
            jbxx['资产总计'] = jbxx['资产总计'].astype(float)
            jbxx['长期负债合计'] = jbxx['长期负债合计'].astype(float)
            jbxx['每股收益'] = jbxx['每股收益'].astype(float)
        jbxx.to_excel(writer,sheet_name='基本指标(元)',index=True)
        writer.save()
        time_end=time.time()
        print("...[%d]use time=%.2f,finish writing Stock =%s data to %s"%(i,time_end-time_start,code,savefileName))


def getStockBaseAccount(code):
    '''
    paramter :
        code - stock code like '000651'
        fileName - xls name like 'test.xls'
    '''
    stocks = getStockBaseInfo(code)
    ret =[]
    for stock in stocks:
        ret.append(stock.getSeries())
    df =pd.DataFrame(ret)
    if(len(df)>0):
        df.set_index(['日期'],inplace=True)
    else:
        print('....%s 没有提取到数据'%code)
    df1 =df
    # df1.to_excel(fileName) 
    return df1

def getStockBaseInfo(stock_code):
    '''
    '''
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    url="http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c"%({'stock_code':stock_code})
    req = request.Request(url=url,headers=headers)
    data = str(urlopen(req).read().decode('GBK'))
    data = data.replace("&nbsp;", "-")
    stock = parse_data(data)
    return stock
def parse_data(urldata):
    '''
    日期,每股净资产,每股收益,每股现金含量,每股资本公积金,固定资产合计,流动资产合计,资产总计,
    长期负债合计,主营业务收入,财务费用,净利润 
    '''
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
            stock = StockAccountBaseInfo(line)
            stocks.append(stock)
            arr = []
    return stocks
class stock_parser(HTMLParser):
    '''
    解析网络响应 -读取财务基本信息
    '''
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

class StockAccountBaseInfo:
    '''
    构建股票财务基本信息字符串
    '''
    def __init__(self,line):
        # 20011231,每股净资产,1.5727,每股收益,0.3438,每股现金含量,11,每股资本公积金,0.5289,
        # 固定资产合计,11,流动资产合计,11,资产总计,11,长期负债合计,16,主营业务收入,11,11,净利润,11
        arr = line.split(",")
        self.day = arr[0].replace("-","") if arr[0]!='-' else '0'   #日期
        self.mgzjc = arr[2] if arr[2]!='-' else '0'                 #每股净资产
        self.mgsy = arr[4] if arr[4]!='-' else '0'                  #每股收益
        self.mgxjhl = arr[6] if arr[6]!='-' else '0'                #每股现金含量                
        self.mgjbgjj = arr[8] if arr[8]!='-' else '0'               #每股资本公积金
        self.gdzchj = arr[10] if arr[10]!='-' else '0'              #固定资产合计
        self.ldzchj = arr[12] if arr[12]!='-' else '0'              #流动资产合计
        self.zchj = arr[14] if arr[14]!='-' else '0'                #资产总计                
        self.cqfzhj = arr[16] if arr[16]!='-' else '0'              #长期负债合计
        self.zyywsr = arr[18] if arr[18]!='-' else '0'              #主营业务收入
        self.cwfy = arr[19] if arr[19]!='-' else '0'                #财务费用
        self.jlr = arr[21] if arr[21]!='-' else '0'                 #净利润
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


# import pandas as pd
# import urllib.request as urllib2
# from bs4 import BeautifulSoup 
# import datetime
class tradeData:
    def getDataQuaterAndYear(self,userDate):
        user_date = datetime.datetime.strptime(userDate, "%Y-%m-%d")
        season =1
        if user_date.month in [1, 2, 3]:
            season =1
        elif user_date.month in [4,5,6]:
            season =2
        elif user_date.month in [7, 8, 9]:
            season =3
        elif user_date.month in [10, 11, 12]:
            season =4
        return user_date.year,season

    def getDataDayUse(self,fName,Code,startDate,endDate,indexFlag='0'):
        '''
        indexFlag ='0' index data
        indexFlag ='1' stock data
        '''
        #确定起始和结束的日期的年份和季度
        dfResult =pd.DataFrame()
        year,season =self.getDataQuaterAndYear(startDate)
        if(indexFlag=='0'):
            dfResult =self.getIndexDayPart(Code,year,season)
        else:
            dfResult =self.getStockDayPart(Code,year,season)
 
        endDateT = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        while(1):
            month =((season+1)*3)
            if(month>12):
                season =1
                month=3
                year =year+1
            cmpDate =datetime.datetime(year,month,1)
            if(cmpDate<endDateT):
                strDate =cmpDate.strftime("%Y-%m-%d")
                
                year,season =self.getDataQuaterAndYear(strDate)

                if(indexFlag=='0'):
                    df0 =self.getIndexDayPart(Code,year,season)
                else:
                    df0 =self.getStockDayPart(Code,year,season)
                # df0 =self.getIndexDayPart(Code,year,season)
                # print(df0)
                if(df0 is None):
                     pass
                else:
                    dfResult =dfResult.append(df0)
            else:
                strDate =cmpDate.strftime("%Y-%m-%d")
                year,season =self.getDataQuaterAndYear(strDate)

                if(indexFlag=='0'):
                    df0 =self.getIndexDayPart(Code,year,season)
                else:
                    df0 =self.getStockDayPart(Code,year,season)

                # df0 =self.getIndexDayPart(Code,year,season)
                if(df0 is None):
                    pass
                else:
                    dfResult =dfResult.append(df0)
                break
        #删除不再开始和结束范围内的数据
        if(dfResult is None):
            return 
        colname_date ='日期'
        dfResult1=dfResult.sort_values(by=[colname_date])
        dfResult1 =dfResult1.reset_index()
        dfResult1 =dfResult1.drop('index',axis =1)
        #改变格式
        # startDate =datetime.datetime.strptime(startDate, "%Y-%m-%d")
        # strStart =startDate.strftime("%Y%m%d")
        strStart =startDate
        # endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        # strEnd =endDate.strftime("%Y%m%d")
        strEnd =endDate

        dfResult1=dfResult1.drop(dfResult1[colname_date][dfResult1[colname_date]<strStart].index)
        dfResult1=dfResult1.drop(dfResult1[colname_date][dfResult1[colname_date]>strEnd].index)

        dfResult1 =dfResult1.reset_index()
        dfResult1 =dfResult1.drop('index',axis =1)
        #将dataframe存入xls文件
        # writer = pd.ExcelWriter(fName)
        # sheetName =Code
        # if(indexFlag=='0'):
        #     sheetName ="Index"+Code
        # dfResult1.to_excel(writer,sheet_name=sheetName)	
        # writer.save()   
        return dfResult1

    def getStockDayPart(self,Code,year,season):  
        '''
        get stock from 163.com
        
        hhttp://quotes.money.163.com/trade/lsjysj_000651.html
        http://quotes.money.163.com/trade/lsjysj_000651.html?year=2019&season=1
        '''
        #判断year和season是不是当前时间,如果是替代url
        now = datetime.datetime.now()
        flag =False
        if(season>1):
            if((now.year ==year) and (now.month<=(season*3)) and (now.month>((season-1)*3))):
                flag =True
        else:
            if((now.year ==year) and (now.month<=(season*3))):
                flag =True

        if(flag==True):
            url ="http://quotes.money.163.com/trade/lsjysj_%s.html"%(Code)
        else:
            url = "http://quotes.money.163.com/trade/lsjysj_%s.html?year=%s&season=%s"%(Code,year,season)
        
        df0 =self.getDataPart(Code,year,season,url)
        return df0

    def getIndexDayPart(self,indexCode,year,season):  
        '''
        get index from 163.com
        http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=2019&season=1
        http://quotes.money.163.com/trade/lsjysj_zhishu_399001.html
        http://quotes.money.163.com/trade/lsjysj_zhishu_399001.html?year=2019&season=1
        '''
        #判断year和season是不是当前时间,如果是替代url
        now = datetime.datetime.now() 
        flag =False
        if(season>1):
            if((now.year ==year) and (now.month<=(season*3)) and (now.month>((season-1)*3))):
                flag =True
        else:
            if((now.year ==year) and (now.month<=(season*3))):
                flag =True

        if(flag==True):
            url ="http://quotes.money.163.com/trade/lsjysj_zhishu_%s.html"%(indexCode)
        else:
            url = "http://quotes.money.163.com/trade/lsjysj_zhishu_%s.html?year=%s&season=%s"%(indexCode,year,season)
        df0 =self.getDataPart(indexCode,year,season,url)
        return df0

    def getDataPart(self,indexCode,year,season,url):
        '''
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)

        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")

        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j=-1
        #read data from 163
        colName =[]
        dataContent =[]
        for row in table0.findAll("tr"):
            cells = row.findAll("th") #获取表格标题
            if(len(cells)>0):
                j=0
                while j <len(cells):
                    colName.append(cells[j].text)
                    j =j+1
                # print(colName)
            else:
                cells = row.findAll("td") #获取表格内容
                j=0
                dfContent =[]
                while j <len(cells):
                    if(j==0):
                        dfContent.append(cells[j].text)
                    else:
                        fNum = cells[j].text.replace(",","").replace("--","0")
                        dfContent.append(float(fNum))
                    j =j+1

                dataContent.append(dfContent)
                   
        oneDf =pd.DataFrame(dataContent,columns=colName)
        return oneDf

# if __name__ == '__main__':
#     test =tradeData()
#     test.getDataDayUse("AAAA.xls","000651","2018-03-01","2019-04-28",'1')
if __name__ == '__main__':
    MainOpt()
    # s = r'<td class=" listview-col-Code"><a href="/sz300256.html">'
    # s = r'<td class=" listview-col-Code"><a href="/\D{2}\d{6}.html">'
    # s = r'<td class=" listview-col-Code"><a href="/(.*).html">'
    # test ='<td class=" listview-col-Code"><a href="/sz300256.html">300256</a></td>'
    # pat = re.compile(s)
    # result = pat.findall(test)
    # print(result)
    # result = re.match(s, test)
    # print(result.group(1))