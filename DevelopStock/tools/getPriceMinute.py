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
UrlBase_Minute ="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=sz000651&date=2019-03-11&page=79"
# UrlBase_History ="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz000651&date=2019-03-08"
UrlBase_History ="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=sz000651&date=2019-03-08&page=7"
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
    def getStockLoop(self,code):
        '''
        获取当天的分时数据
        '''
        now_time = datetime.datetime.now()
        dateL =now_time.strftime('%Y-%m-%d')
        startL =datetime.datetime.strptime(dateL+ " 09:25:00", "%Y-%m-%d %H:%M:%S")
        sSpan =(now_time -startL)#计算距离 09:25:00 的时间
        idTSpan =math.ceil(sSpan.seconds/3.0)#每三秒一个界面 共同79个界面
        if(idTSpan>=79):
            # idTSpan =3
            k=1
            dk=pd.DataFrame()
            while(k<=idTSpan):
                data =self.getStockMiuteTrade(code,dateL,k)
                # columns =data.columns
                # data =np.array(data)
                # data =data.tolist()#
                dk =dk.append(data,ignore_index=True)
                k =k+1
            df =dk
            print(df)
        return df,dateL
    def getStockLoopToday(self,code):
        dk,day =self.getStockLoop(code)
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()

    def getStockLoopHistory(self,code,day):
        now_time = datetime.datetime.now()
        # nowTimeStr =now_time.strftime('%Y-%m-%d')
        destDay =datetime.datetime.strptime(day,"%Y-%m-%d")
        dayDelay =now_time - destDay
        dk=pd.DataFrame()
        if(dayDelay.day>=1):
            idTSpan =79
            k=1
            
            while(k<=idTSpan):
                data =self.getStockMiuteTrade(code,day,k)
                dk =dk.append(data,ignore_index=True)
                k =k+1
            
        else:
            dk,today =self.getStockLoop(code)
        pathName ="%s%s(%s).xls"%(self.destPath,code,day)
        write = pd.ExcelWriter(pathName)
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dk.to_excel(write,sheet_name=code,index=True)
        write.save()  
        return dk
    def saveToXls(self,pathName,code,df):
        write = pd.ExcelWriter(pathName)
        # 将数据按照交易日期从近到远排序
        # df.sort_values('date', ascending=False, inplace=True)
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        df.to_excel(write,sheet_name=code,index=True)
        write.save()              
   
    def getStockMiuteTrade(self,code,dateL,id):
        '''
        获取指定股票的实时数据:
            dataL like'2019-03-08'
            id 1~79
        '''
        #
        UrlBase_Minute ="http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradedetail.php?symbol=%s&date=%s&page=%s"
        content =self.urlOpenContent(UrlBase_Minute%(code,dateL,id))
        soup = BeautifulSoup(content,features="lxml")
        div = soup.find("div",{"class":"dataOuter"})        
        table =div.find('table',{"class":"datatbl"})

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
        
        return df
        
        
if __name__ == '__main__':
    Main =StockMinuteData()
    Main.getStockLoop('sz000651')