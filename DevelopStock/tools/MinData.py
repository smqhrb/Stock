'''
读取股票的分时数据
    1.历史
    2.当天实时
'''
import random
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
    def __init__(self,destPath=".\\Minutes\\",uiDlg =None):
        self.uiDlg =uiDlg
        # self.UiList =[]
        # self.UiProcessBar =0
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            pass
        else:
            os.mkdir(destPath)
        pass  
    def urlOpenContent(self,url):
        '''
        parameter:
            url is made by urlBase urlfix
        return content
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        while True:
            try:
                content = urllib2.urlopen(req,timeout=5).read()
                time.sleep(random.randint(0,3))
                break
            except:
                print("超时重试")
                # self.UiList.append("超时重试") 
                self.uiDlg.addListViewMessage("超时重试")
        return content
    def getStockLoop(self,code):
        '''
        获取当天的分时数据
        '''
        now_time = datetime.datetime.now()
        dateL =now_time.strftime('%Y-%m-%d')
        startL =datetime.datetime.strptime(dateL+ " 09:25:00", "%Y-%m-%d %H:%M:%S")
        dateTimeNow =now_time.strftime("%Y-%m-%d %H:%M:%S")
        startTime =startL.strftime("%Y-%m-%d %H:%M:%S")
        if(dateTimeNow<startTime):
            print('-----%s<%s,没有开始交易'%(dateTimeNow,startTime))
            self.uiDlg.addListViewMessage('-----%s<%s,没有开始交易'%(dateTimeNow,startTime))
            return pd.DataFrame()
        sSpan =(now_time -startL)#计算距离 09:25:00 的时间
        idTSpan =math.ceil(sSpan.seconds/3.0)#每三秒一个界面 共同79个界面
        if(idTSpan>=79):
            idTSpan =79
        k=1
        dk=pd.DataFrame()
        while(k<=idTSpan):
            data =self.getStockMiuteTrade(code,dateL,80-k,'1')
            percent = round(1.0 * k / idTSpan * 100,2)
           
            self.uiDlg.setProcessBarPos(percent)
            print('        当前进度 : %s [%d/%d]'%(str(percent)+'%',k,idTSpan),end='\r')
            dk =dk.append(data,ignore_index=True)
            k =k+1
        df =dk
        return df,dateL
    def getStockLoopToday(self,code):
        print("------开始读取股票(%s)今天的分时数据"%code)
        self.uiDlg.addListViewMessage("------开始读取股票(%s)今天的分时数据"%code)
        dk,day =self.getStockLoop(code)
        print("------结束读取股票(%s)今天的分时数据"%code)
        self.uiDlg.addListViewMessage("------结束读取股票(%s)今天的分时数据"%code)
        if(len(dk)<=0):
            return
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()
        print("------股票(%s)今天的分时数据,写入%s"%(code,pathName))
        self.uiDlg.addListViewMessage("------股票(%s)今天的分时数据,写入%s"%(code,pathName))

    def getStockLoopHistory(self,code,day):
        print("------开始读取股票(%s)%s的分时数据"%(code,day))
        self.uiDlg.addListViewMessage("------开始读取股票(%s)%s的分时数据"%(code,day))
        now_time = datetime.datetime.now()
        destDay =datetime.datetime.strptime(day,"%Y-%m-%d")
        dayDelay =now_time - destDay
        dk=pd.DataFrame()
        if(dayDelay.days>=1):
            idTSpan =79
            k=1
            
            while(k<=idTSpan):
                data =self.getStockMiuteTrade(code,day,80 -k,'2')
                percent = round(1.0 * k / idTSpan * 100,2)
                self.uiDlg.setProcessBarPos(percent)
                print('        当前进度 : %s [%d/%d]'%(str(percent)+'%',k,idTSpan),end='\r')

                if(len(data)>0):
                    dk =dk.append(data,ignore_index=True)
                k =k+1
            
        else:
            dk,day =self.getStockLoop(code)
        print("------结束读取股票(%s)%s的分时数据"%(code,day))
        self.uiDlg.addListViewMessage("------结束读取股票(%s)%s的分时数据"%(code,day))
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()  
        print("------股票(%s)%s的分时数据,写入%s"%(code,day,pathName))
        self.uiDlg.addListViewMessage("------股票(%s)%s的分时数据,写入%s"%(code,day,pathName))
        return dk
      
   
    def getStockMiuteTrade(self,code,dateL,id,type='1'):
        '''
        获取指定股票的实时数据:
            dataL like'2019-03-08'
            id 1~79
        '''
        #
        
        if(type=='1'):
            UrlBase ="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=%s&date=%s&page=%s"
        else:
            UrlBase ="http://market.finance.sina.com.cn/transHis.php?symbol=%s&date=%s&page=%s"
        content =self.urlOpenContent(UrlBase%(code,dateL,id))
         
        if(len(content)<=0):
            df =pd.DataFrame()
            return df
        try:
            soup = BeautifulSoup(content,features="lxml")
            div = soup.find("div",{"class":"dataOuter"})        
            table =soup.find('table',{"class":"datatbl"})
            #获取列名
            thead =table.find('thead')
            thead_th =thead.findAll('th')
            thead_td =thead.findAll('td')
            i =0
            columnsName =[]
            while(i<len(thead_th)):
                columnsName.append(thead_th[i].text)
                i =i+1
            i=0
            while(i<len(thead_td)):
                columnsName.append(thead_td[i].text)
                i =i+1
            #
            #获取数据
            tbody =table.find('tbody')
            tbody_tr =tbody.findAll('tr')
            i=0
            tbody_data =[]
            while(i<len(tbody_tr)):
                rowData =[]
                tbody_tr_th =tbody_tr[i].findAll('th')
                k=0
                while(k<len(tbody_tr_th)):
                    rowData.append(tbody_tr_th[k].text)
                    k =k+1
                
                tbody_tr_td =tbody_tr[i].findAll('td')
                k=0
                while(k<len(tbody_tr_td)):
                    rowData.append(tbody_tr_td[k].text)
                    k =k+1
                tbody_data.append(rowData)
                i =i+1
            df =pd.DataFrame(tbody_data,columns=columnsName)
        except:
            df =pd.DataFrame()
        return df
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
                print("|   -f stockList.txt       [从文件stockList.txt 读取所有的股票代码，代码的形式 sh601800 or sz300298 or sz000882]      ")
                print("|   -t 1                   [类型 1-读取 当天;2-读取历史                                                       ]        ")
                print("|   -s 2017-01-11          [开始时间,形式 YYYY-MM-DD                                                         ]                       ")
                print("|   -e 2018-01-11          [结束时间,形式 YYYY-MM-DD                                                         ]                 ")
                print("|                     ")
                print("|   举例子:")
                print("|      例子 1: 读取在文件stockList.txt中的所有股票当天的分时数据")
                print("|           python MinData.py -t 1 -f stockList.txt")
                print("|      例子 2: 读取在文件stockList.txt中的所有股票的日期从2019-03-04到2019-03-06分时数据")
                print("|           python MinData.py -t 2 -f stockList.txt -s 2019-03-04 -e 2019-03-06")
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
                    readDay =startDay
                    while(k<=dayDelay.days):
                        day =readDay.strftime('%Y-%m-%d')
                        readDay =readDay + timedelta(days=1)
                        self.getStockLoopHistory(code,day)
                        k =k+1
            print(".................全部结束.................")
        else:
            print("...在文件中没有股票代码或者文件不存在 ,退出....")
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
    Main.MainOpt()
