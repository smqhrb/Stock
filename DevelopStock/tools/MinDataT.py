'''
读取股票的分时数据
    1.历史
    2.当天实时
'''
import tushare as ts
import os,time,sys,re,datetime
import math
from datetime import timedelta
from urllib import request
from urllib import parse
from urllib.request import urlopen
import numpy as np
import pandas as pd
import xlwt
from bs4 import BeautifulSoup 
import urllib.request as urllib2
import getopt
class StockMinuteData:
    def __init__(self,destPath=".\\Minutes\\"):
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            pass
        else:
            os.mkdir(destPath)
        pass  
    def Get_Stock_List(self):
        '''
        #获取股票列表
        #code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
        # fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
        ''' 
               
        if os.path.exists("stockListAccount.xls") is True:     #判断文件 stockList.xls 是否存在,如果存在 则从文件中读取
            print("------开始读取stockListAccount股票信息")
            self.df =pd.read_excel('stockListAccount.xls',dtype={'code':'str'})
            self.df =self.df.sort_values(by=['code'])
            self.df =self.df.set_index('code')
            
            print("------结束读取stockListAccount.xls股票信息")
        else:
            print("------开始读取网上股票信息")
            self.df = ts.get_stock_basics()             #不存在则从网上读取
            self.df =self.df.sort_values(by=['code'])
            write = pd.ExcelWriter('stockListAccount.xls')     #存储到文件  stockList.xls  
            self.df.to_excel(write,index=True)
            write.save()
            print("------结束读取网上股票信息")

        return self.df      
    def urlOpenContent(self,url):
        '''
        parameter:
            url is made by urlBase urlfix
        return content
        '''
        # url =urlBase%(urlfix)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return 
        return content
    def getStockLoopToday(self,code):
        print("------开始读取股票(%s)今天的分时数据"%code)
        dk = ts.get_realtime_quotes(code)
        print("------结束读取股票(%s)今天的分时数据"%code)
        if(len(dk)<=0):
            return
        now_time = datetime.datetime.now()
        day =now_time.strftime('%Y-%m-%d')
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()
        print("------股票(%s)今天的分时数据,写入%s"%(code,pathName))

    def getStockLoopHistory(self,code,day):
        print("------开始读取股票(%s)%s的分时数据"%(code,day))
        dk = ts.get_tick_data(code,day,src='tt')
        df = ts.get_tick_data('600848',date='2018-12-12',src='tt')

        
        print("------结束读取股票(%s)%s的分时数据"%(code,day))
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()  
        print("------股票(%s)%s的分时数据,写入%s"%(code,day,pathName))
        return dk
    def MainOpt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:],'f:s:e:t:h',['files=','start=','end=','type=','help'])
        except getopt.GetoptError: 
            print(getopt.GetoptError)
            sys.exit()

        files=""
        start =""
        end =""
        rType ="1"
        for o, a in opts:
            if o in ("-h", "--help"):
                print("---------help content------------------------------------------------------")
                print("|   -f stockList.txt     [get all stock data from config file (stockList.txt )      ")
                print("|                        stock code like sh601800 or sz300298 or sz000882]")
                print("|   -t 1                 [read type 1-read history;2-read today]        ")
                print("|   -s 2017-01-11          [start time,format YYYY-MM-DD]                       ")
                print("|   -e 2018-01-11          [end   time,format YYYY-MM-DD]                 ")
                print("|   for example:")
                print("|      example 1: read today data of stocks at file (stockList.txt)")
                print("|           python MinDataT.py -t 1 -f stockList.txt")
                print("|      example 2: read minute:second stock data from 2017-01-11 to 2018-01-11")
                print("|           python MinDataT.py -t 2 -f stockList.txt -s 2017-01-11 -e 2018-01-11")
                print("---------------------------------------------------------------------------------")
                sys.exit()
            elif o in ("-f", "--files"):
                files = a
            elif o in ("-t","--type"):
                rType =a
            elif o in ("-s","--start"):
                start =a
            elif o in ("-e","--end"):
                end =a
            else:
                sys.exit()
        print("test test")
        start ='2017-01-11'
        end ='2018-01-11'
        rType ='2'
        files ='stockList.txt'
        print("Please confirm xls file not to be covered in current folder")
        print("Continue? Please input 'y' to continune,'n' to end this program.")
        str = input("Enter your input: ")
        if str=='n':
            exit()
        elif str=='y':
            pass

        if len(files)>0:
            print("configure file name ="+files)

            stockCodeList =self.readStockList(files)
            for code in stockCodeList:
                if rType =='1' :
                    self.getStockLoopToday(code)
                else:
                    print("------[开始时间%s,结束时间%s]"%(start,end))
                    startDay =datetime.datetime.strptime(start,"%Y-%m-%d")
                    endDay =datetime.datetime.strptime(end,"%Y-%m-%d")
                    dayDelay = endDay -startDay
                    k=0
                    while(k<dayDelay.days):
                        readDay =startDay + timedelta(days=1)
                        day =readDay.strftime('%Y-%m-%d')
                        self.getStockLoopHistory(code,day)
            print("...end.................")
        else:
            print("...without stock code ,program end....")
            exit()        
    def readStockList(self,fname=''):
        contents =[]
        f = open(fname)
        lines = f.readlines()
        for code in lines:
            k =code.strip()
            if len(k)>0:
                contents.append(k)
        f.close()
        print("....Stock Code List............")
        print(contents)
        return contents            
if __name__ == '__main__':
    Main =StockMinuteData()
    # Main.MainOpt()
    Main.getStockLoopHistory('000651','2017-03-31')
    # Main.getStockMiuteTrade('sz000651','2017-03-31','2','2')
    # Main.getTushare()