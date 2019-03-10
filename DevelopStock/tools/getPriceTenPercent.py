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
import json
from datetime import timedelta
# stockHsUp ="http://vip.stock.finance.sina.com.cn/mkt/#stock_hs_up%s"
stockHsUp ="http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=40&sort=changepercent&asc=0&node=hs_a&symbol=&_s_r_a=auto"
# stockHsUp ="http://hq.sinajs.cn/rn=b5zw4&amp;list=sz000630,sz002131,sz002505,sh600157,sh600139,sh601326,sz300043,sh600020,sz002610,sz300255,sh603011,sz300291,sh600293,sz000633,sh601598,sz002477,sh600552,sz002519,sh600868,sh600589,sh603111,sz002711,sh601016,sz000795,sh600736,sz002356,sh600651,sh601890,sz000607,sz002175,sh600572,sz002600,sz300352,sz000810,sz300293,sz002143,sz002316,sz300249,sz300081,sz300160%s"
class stockUpTenPercent:
    '''
    目标:近40天涨停全部股票 按文件单独存储到xls文件中
    输入:近40天涨停全部股票
    输出:换手率 成交量 流通市值 量比 涨跌幅,
        ma5 ma10 ma20 ma31 ma60 ma120 dif dea macd
        (ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
        m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率
    '''
    def __init__(self,destPath=".\\Day40Top\\"):
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
    def urlOpenContent(self,urlBase,urlfix=""):
        '''
        parameter:
            url is made by urlBase urlfix
        return content
        '''
        url =urlBase%(urlfix)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return 
        return content

    def getStockGb(self,code):
        '''
        获取流动股本信息
        '''
        # stockGbbd ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/000001.phtml'#股本变动
        stockGbbd ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/%s.phtml'#股本变动
        content =self.urlOpenContent(stockGbbd,code)
        soup = BeautifulSoup(content,features="lxml")
        div = soup.find("div",{"class":"tagmain"})
        tableAll =div.findAll('table')
        i =0
        df =pd.DataFrame()
        data =[]
        dateL =[]
        sc =[]
        while(i<len(tableAll)):
            tbody =tableAll[i].find('tbody')
            tr =tbody.findAll('tr')
            date =tr[0].findAll('td')#日期
            stockCount =tr[6].findAll('td')#股数
            j =1
            while(j<len(date)):
                dateL.append(date[j].text)
                sc.append(stockCount[j].text.replace(' 万股',''))
                j =j+1
            i =i+1
        data.append(dateL)
        data.append(sc)
        df =pd.DataFrame(data) 
        df =df.T
        df =pd.DataFrame(df,columns=['date','stockCount']) #日期 ,流通股本
        return df




        

    def stock_hs_up(self,rcDay =40):
        '''
        换手率 成交量 流通市值 量比 涨跌幅,
        ma5 ma10 ma20 ma31 ma60 ma120 dif dea macd
        (ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
        m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率
        '''
        # content =self.urlOpenContent(stockHsUp,'1')

        # soup = BeautifulSoup(content,features="lxml")
        # print(soup.p.text)
        # retContent = soup.p.text
        # retContent =retContent.replace('symbol','"symbol"')
        # retContent =retContent.replace('code','"code"')
        # retContent =retContent.replace('name','"name"')
        # retContent =retContent.replace('trade','"trade"')
        # retContent =retContent.replace('pricechange','"pricechange"')
        # retContent =retContent.replace('changepercent','"AA"')#?
        # retContent =retContent.replace('buy','"buy"')
        # retContent =retContent.replace('sell','"sell"')
        # retContent =retContent.replace('settlement','"settlement"')
        # retContent =retContent.replace('open','"open"')
        # retContent =retContent.replace('high','"high"')
        # retContent =retContent.replace('low','"low"')
        # retContent =retContent.replace('volume','"volume"')
        # retContent =retContent.replace('amount','"amount"')
        # retContent =retContent.replace('ticktime','"ticktime"')
        # retContent =retContent.replace('per','"per"')#
        # retContent =retContent.replace('pb','"pb"')
        # retContent =retContent.replace('mktcap','"mktcap"')
        # retContent =retContent.replace('nmc','"nmc"')
        # retContent =retContent.replace('turnoverratio','"turnoverratio"')
        # retContent =retContent.replace('"AA"','"changepercent"')
        # text = json.loads(retContent)
        # pd.DataFrame(text)
        # print(text)   
#
        now_time = datetime.datetime.now()#现在
        end =now_time.strftime('%Y%m%d')
        day40_time =now_time -timedelta(days=rcDay)#40天前日期
        start =day40_time.strftime('%Y%m%d')
#
        df_Code = self.Get_Stock_List() 
    
        for Code in df_Code.index:
            Name =df_Code.loc[Code,'name']
            # stock_data=ts.get_k_data(Code,start=startDay,end=endDay)#读取股票数据
            stock_data=ts.get_k_data(Code)
            # 将数据按照交易日期从远到近排序
            stock_data.sort_values('date', inplace=True)
            #volumn ratio 量比
            stock_data['vol ratio'] =stock_data['volume']/stock_data['v_ma5']
            # stock_data[换手率]=
            # stock_data[流通市值]=
            # ========== DIF DEA MACD
            nDif,nDea,nMacd =self.calcMacd(stock_data)
            stock_data['DIF'] =nDif
            stock_data['DEA'] =nDea
            stock_data['MACD'] =nMacd
            # ========== 计算移动平均线
            # 分别计算5日,10日,20日,31日,60日,120日的移动平均线
            ma_list = [5, 10,20,31,60,120]
            # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
            for ma in ma_list:
                stock_data['MA_' + str(ma)] = stock_data['close'].rolling(ma).mean()
            # 计算指数平滑移动平均线EMA
            for ma in ma_list:
                stock_data['EMA_' + str(ma)] = stock_data['close'].ewm(span=ma).mean() 
            #(ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
            stock_data['Glue20-31-60']= stock_data['MA_20'] -stock_data['MA_31'] -stock_data['MA_60']
            stock_data['Glue31-60-120']= stock_data['MA_31'] -stock_data['MA_60'] -stock_data['MA_120']

            #
            write = pd.ExcelWriter(Code+"("+Name+").xls")
            # 将数据按照交易日期从近到远排序
            stock_data.sort_values('date', ascending=False, inplace=True)
            # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
            stock_data.to_excel(write,sheet_name=Code,index=True)
            write.save()
            break

    def calcMacd(self,data,fast_period=12,slow_period=26,signal_period=9): 
        # data['close'] -- 收盘价 
        # 收盘价按照日期升序( data['date'] )排列 
        # 返回值都是 Series 
        fast_ewm=data['close'].ewm(span=fast_period).mean() 
        slow_ewm=data['close'].ewm(span=slow_period).mean() 
        dif=fast_ewm-slow_ewm 
        dea=dif.ewm(span=signal_period).mean() 
        # 一般概念里，macd柱是 (dif-dea)*2，实际上只是为了扩大显示效果 
        # # 实测后发现，也可以不乘以2，效果也足够清楚了 
        macd=(dif-dea)*2 
        # 将bar 分成红绿柱分别导出数据， 
        return dif,dea,macd
if __name__ == '__main__':
    Test =stockUpTenPercent()
    Test.getStockGb('000651')
    # Test.stock_hs_up()

