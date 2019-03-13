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
        dateL =[]#日期
        sc =[]#股数
        while(i<len(tableAll)):
            tbody =tableAll[i].find('tbody')
            tr =tbody.findAll('tr')
            date =tr[0].findAll('td')#日期
            stockCount =tr[6].findAll('td')#股数
            j =1
            while(j<len(date)):
                dateL.append(date[j].text)
                stCC =stockCount[j].text.replace(' 万股','')
                stCC =stCC.replace('--','0')
                sc.append(stCC)
                j =j+1
            i =i+1

        arr =np.array(sc)
        float_arr = arr.astype(np.float64)

        data={"date":dateL,'stockCnt':float_arr}
        df =pd.DataFrame(data) 
        df.sort_values('date', inplace=True)

        return df

    def stock_hs_up(self,rcDay =40):
        '''
        换手率 成交量 流通市值 量比 涨跌幅,
        ma5 ma10 ma20 ma31 ma60 ma120 dif dea macd
        (ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
        m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率

        [date open	close	high	low	volume	code	exchange	FlowOfEquity	v_ma5	QRR	turnover	
        amount	
        DIF	DEA	MACD	
        MA_5	MA_10	MA_20	MA_31	MA_60	MA_120	
        EMA_5	EMA_10	EMA_20  EMA_31	EMA_60	EMA_120	
        Glue20-31-60	Glue31-60-120]

        exchange:涨幅(%)
        FlowOfEquity :流动股本(万股)
        QRR:量比
        turnover:换手率
        amount:流通市值
        '''

        now_time = datetime.datetime.now()#现在
        end =now_time.strftime('%Y%m%d')
        day40_time =now_time -timedelta(days=rcDay)#40天前日期
        start =day40_time.strftime('%Y%m%d')
#
        df_Code = self.Get_Stock_List() 
        codeCntTop40 =0
        for Code in df_Code.index:
            Name =df_Code.loc[Code,'name']
            industry =df_Code.loc[Code,'industry']
            area =df_Code.loc[Code,'area']
            pathName = "%s%s(%s_%s_%s).xls"%(self.destPath,Code,Name,industry,area)

            # stock_data=ts.get_k_data(Code,start=startDay,end=endDay)#读取股票数据
            stock_data=ts.get_k_data(Code)
            # 将数据按照交易日期从远到近排序
            stock_data.sort_values('date', inplace=True)
            #判定是否在最近40天
            stock_data['exchange'] =(stock_data['close']-stock_data['close'].shift(1))/stock_data['close'].shift(1)
            check40 =stock_data[0-rcDay:]
            ZT =0.098 #涨停阈值
            
            check40T =check40.loc[check40.exchange>ZT]
            if(len(check40T)==0):
                continue
            codeCntTop40 =codeCntTop40+1
            if os.path.isfile(pathName):
                print("-----%s:%s 已经存在"%(codeCntTop40,pathName))
                continue
            print('------%s 正在读取近40天涨停的股票之一 :%s(%s)------'%(codeCntTop40,Code,Name))
            stockCountB =self.getStockGb(Code)#流动股本
            loop =0
            stock_data['FlowOfEquity'] =0
            while loop<len(stockCountB):
                stock_data.loc[stock_data.date>=stockCountB['date'].iloc[loop],['FlowOfEquity']]=stockCountB['stockCnt'].iloc[loop]
                loop =loop+1
            
            #volumn ratio 量比
            stock_data['v_ma5'] =stock_data['volume'].rolling(5).mean()
            stock_data['QRR'] =stock_data['volume']/stock_data['v_ma5']#量比
            stock_data['turnover']= stock_data['volume']/stock_data['FlowOfEquity']#换手率
            stock_data['amount']=stock_data['close']*stock_data['FlowOfEquity']#流通市值
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
            # M5:=MA(C,5);
            # M10:=MA(C,10);
            # M20:=MA(C,20);
            # A:=MAX(M5,MAX(M10,M20));
            # B:=MIN(M5,MIN(M10,M20));
            # 三线粘合:=(A-B)/B*100
            #N:=3;
            stock_data['Glue20-31-60'] =0
            A =stock_data[['MA_20','MA_31','MA_60']].max(axis=1)
            B =stock_data[['MA_20','MA_31','MA_60']].min(axis=1)
            stock_data['Glue20-31-60'] =(A-B)/B*100
            stock_data['Glue31-60-120'] =0
            A =stock_data[['MA_31','MA_60','MA_120']].max(axis=1)
            B =stock_data[['MA_31','MA_60','MA_120']].min(axis=1)     
            stock_data['Glue31-60-120'] =(A-B)/B*100      
            #####
            #  m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率

            stock_data['Slope_M5'] =self.ma_slope(stock_data['MA_5'])#np.arctan2(((stock_data['MA5']/REF_MA5)-1)*100)*180/3.14115926
            stock_data['Slope_M10'] =self.ma_slope(stock_data['MA_10'])#np.arctan2(((stock_data['MA10']/REF_MA10)-1)*100)*180/3.14115926
            stock_data['Slope_M20'] =self.ma_slope(stock_data['MA_20'])#np.arctan2(((stock_data['MA20']/REF_MA20)-1)*100)*180/3.14115926
            stock_data['Slope_M31'] =self.ma_slope(stock_data['MA_31'])#np.arctan2(((stock_data['MA31']/REF_MA31)-1)*100)*180/3.14115926
            stock_data['Slope_M60'] =self.ma_slope(stock_data['MA_60'])#np.arctan2(((stock_data['MA60']/REF_MA60)-1)*100)*180/3.14115926
            stock_data['Slope_M120'] =self.ma_slope(stock_data['MA_120'])#np.arctan2(((stock_data['MA5']/REF_MA5)-1)*100)*180/3.14115926
            print('------%s 完成读取近40天涨停的股票之一 :%s(%s)------'%(codeCntTop40,Code,Name))
            #
            
            write = pd.ExcelWriter(pathName)
            # 将数据按照交易日期从近到远排序
            stock_data.sort_values('date', ascending=False, inplace=True)
            # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
            stock_data.to_excel(write,sheet_name=Code,index=True)
            write.save()
            print('------%s 近40天涨停的股票之一 :%s(%s) 写入%s------'%(codeCntTop40,Code,Name,pathName))
            # break
    def ma_slope(self,MA):
        '''
        MA1:=MA(CLOSE,10);
        m10斜率:=(ATAN((MA1/REF(MA1,1)-1)*100)*180/3.14115926);
        '''
        REF_MA =MA.shift(1)
        slopeMa =np.arctan2((MA -REF_MA)*100,REF_MA)*180/3.1415926
        return slopeMa

    def glue3K(self,df):
        '''
        三线粘合
            
        M5:=MA(C,5);
        M10:=MA(C,10);
        M20:=MA(C,20);
        A:=MAX(M5,MAX(M10,M20));
        B:=MIN(M5,MIN(M10,M20));
        三线粘合:=LLV((A-B)/B*100<N,3) AND M5>REF(M5,1);
        REF代表过去的意思，用法是：REF(X,A),引用A周期前的X值例如：REF(CLOSE,1)表示上一周期的收盘价，在日线上就是昨收。
        '''
       

 
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
    Main =stockUpTenPercent()
    Main.stock_hs_up()

