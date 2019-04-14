############################################
#   QT 批量处理通达信二进制数据 进入 数据库 
#   计算均线 布林 MACD  均线斜率 均线粘合  日 周 月 的 计算方法 
#   PY计算出来的结果 和通达信的 
#   PY  能否先 做个挑选和行业 和板块 的龙头股 结合龙虎榜 经常上榜的股票
############################################
import os
from struct import unpack
import pandas as pd
import datetime
import xlwt
import xlrd
import numpy as np
from dbOper import *
#from numba import jit
#
# import urllib.request as urllib2

# from bs4 import BeautifulSoup 
# from html.parser import HTMLParser  
# from urllib import request
# from urllib import parse
# from urllib.request import urlopen
#

class TdxData:
    '''
    读取通达信的日线数据
    '''
    def __init__(self):
        '''
        初始化 并且连接数据库
        '''
        self.mydb =mysqlDB()#连接数据库
        pass
    # def __getstate__(self):
    #     """ This is called before pickling. """
    #     state = self.__dict__.copy()
    #     # del state['mydb']
    #     return state

    # def __setstate__(self, state):
    #     """ This is called while unpickling. """
    #     self.__dict__.update(state)

    def getDbStatus(self):
        '''
        返回数据库状态
        '''
        return self.mydb.getDbStatus()
        # pass

    def ifFileExist(self,fn):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(fn)==False):
            return False
        else:
            return True  
    #@jit
    def day2csv(self,source_dir, file_name, target_dir,target_prefix=""):
        '''
        获取输入级从通达信的日线数据
        日线数据位于：new_tdx/vipdoc/sz/lday/,new_tdx/vipdoc/sh/lday/
        '''
        # 以二进制方式打开源文件
        srFn = source_dir +os.sep+  file_name 
        code =file_name[2:8]
        if(self.ifFileExist(srFn) ==False):
            return False

        source_file = open(srFn, 'rb')#读取日线数据
        buf = source_file.read()
        source_file.close()
    
        # 打开目标文件，后缀名为xls
        target_file = target_dir + os.sep + target_prefix +file_name + '.xls'
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        begin = 0
        end = 32

        dayTrade =[]
        
        for i in range(rec_count):
            # 将字节流转换成Python数据格式
            # I: unsigned int
            # f: float
            a = unpack('IIIIIfII', buf[begin:end])
            date =str(a[0]) #交易日期
            date_time = datetime.datetime.strptime(date,'%Y%m%d')
            date= date_time.strftime('%Y-%m-%d')
            openPrice =(a[1] / 100.0)#开盘价
            highPrice =(a[2] / 100.0)#最高价
            lowPrice =(a[3] / 100.0)#最低价
            closePrice =(a[4] / 100.0)#收盘价
            amount =(a[5] / 10.0)#成交金额
            volume =(a[6])#成交量

            dayTrade.append([code,date,openPrice,highPrice,lowPrice,closePrice,amount,volume])
            begin += 32
            end += 32
        dayTdx =pd.DataFrame(dayTrade)
        #指定列名
        dayTdx.rename(columns={0:'code',1:'date',2:'open',3:'high',4:'low',5:'close',6:'amount',7:'volume'},inplace=True)#
        
        dayTdx.set_index(pd.DatetimeIndex(pd.to_datetime(dayTdx.t)), inplace=True)
        # # 周数据
        weekTdx =self.periodChange(dayTdx,'W')
        # 月数据dayTdx.sort_values('date', ascending=False, inplace=True)
        monthTdx =self.periodChange(dayTdx,'M')
        #计算均线 布林 MACD  均线斜率 均线粘合

        write = pd.ExcelWriter(target_file)
        # 将数据按照交易日期从近到远排序
       
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dayTdx =self.indicatorCalc(dayTdx)
        weekTdx =self.indicatorCalc(weekTdx)
        monthTdx =self.indicatorCalc(monthTdx)
        
        self.mydb.to_sql(dayTdx,'day_k')#写入数据库
        dayTdx.to_excel(write,sheet_name=file_name)#写入文件
        self.mydb.to_sql(weekTdx,'week_k')#写入数据库
        weekTdx.to_excel(write,sheet_name='周')#写入文件
        self.mydb.to_sql(monthTdx,'month_k')#写入数据库
        monthTdx.to_excel(write,sheet_name='月')#写入文件
        write.save()#存盘
        return True

    def fz2csv(self,source_dir, file_name, target_dir):
        '''
        通达信5分钟线*.lc5文件和*.lc1文件
        '''
        source_file = open(source_dir + os.sep + file_name, 'rb')
        buf = source_file.read()
        source_file.close()

        # 打开目标文件，后缀名为xls
        target_file = target_dir + os.sep + file_name + '.xls'
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        begin = 0
        end = 32
        minTrade =[]

        for i in range(rec_count):
            a=unpack('hhfffffii',buf[begin:end])
            minTrade.append([str(int(a[0]/2048)+2004)+'-'+str(int(a[0]%2048/100)).zfill(2)+'-'+str(a[0]%20480).zfill(2),str(int(a[1]/60)).zfill(2)+':'+str(a[1]%60).zfill(2)+':00',a[2],a[3],a[4],a[5],a[6],a[7]])
            end=end+32
            end=end+32
        minTdx = pd.DataFrame(minTrade, columns=['date','time','open','high','low','close','amount','volume'])
        minTdx.sort_values('date', ascending=False, inplace=True)
        minTdx.to_excel(target_file,sheet_name=file_name)

    #@jit
    def indicatorCalc(self,stock_data):
        '''
        计算指数 MACD MA 三线粘合 斜率
        '''
        nDif,nDea,nMacd =self.calcMacd(stock_data)#MACD(12,26,9)
        stock_data['DIF'] =nDif
        stock_data['DEA'] =nDea
        stock_data['MACD'] =nMacd
        # ========== 计算移动平均线
        # 分别计算5日,10日,20日,31日,60日,120日的移动平均线
        ma_list = [5, 10,20,31,60,120]
        # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
        for ma in ma_list:
            stock_data['MA_' + str(ma)] = stock_data['close'].rolling(ma).mean()

        #(ma20, ma31, ma60)(ma31,ma60,ma120) 三线粘合值
        # M5:=MA(C,5);
        # M10:=MA(C,10);
        # M20:=MA(C,20);
        # A:=MAX(M5,MAX(M10,M20));
        # B:=MIN(M5,MIN(M10,M20));
        # 三线粘合:=(A-B)/B*100
        #N:=3;
        stock_data['Glue20_31_60'] =0
        A =stock_data[['MA_20','MA_31','MA_60']].max(axis=1)
        B =stock_data[['MA_20','MA_31','MA_60']].min(axis=1)
        stock_data['Glue20_31_60'] =(A-B)/B*100
        stock_data['Glue31_60_120'] =0
        A =stock_data[['MA_31','MA_60','MA_120']].max(axis=1)
        B =stock_data[['MA_31','MA_60','MA_120']].min(axis=1)     
        stock_data['Glue31_60_120'] =(A-B)/B*100      
        #####
        #  m5斜率 m10斜率 m20斜率 m31斜率 m60斜率 m120斜率
        stock_data['Slope_M5'] =self.ma_slope(stock_data['MA_5'])
        stock_data['Slope_M10'] =self.ma_slope(stock_data['MA_10'])
        stock_data['Slope_M20'] =self.ma_slope(stock_data['MA_20'])
        stock_data['Slope_M31'] =self.ma_slope(stock_data['MA_31'])
        stock_data['Slope_M60'] =self.ma_slope(stock_data['MA_60'])
        stock_data['Slope_M120'] =self.ma_slope(stock_data['MA_120'])
        #布林线
        self.bollinger(stock_data,20)#BOLL(20)
        return stock_data

   # @jit
    def ma_slope(self,MA):
        '''
        MA1:=MA(CLOSE,10);
        m10斜率:=(ATAN((MA1/REF(MA1,1)-1)*100)*180/3.14115926);
        '''
        REF_MA =MA.shift(1)
        slopeMa =np.arctan2((MA -REF_MA)*100,REF_MA)*180/3.1415926
        return slopeMa   

    def periodChange(self,stock_data,period_type):
        '''
        由日线数据转化为周 或者月数据
        period_type 决定转换类型
        '''
        #设定转换周期period_type  转换为周是'W',月'M',季度线'Q',五分钟'5min',12天'12D'
        #period_type = 'W'
        #进行转换，周线的每个变量都等于那一周中最后一个交易日的变量值
        period_stock_data = stock_data.resample(period_type).last()#,how='last')
        #周线的change等于那一周中每日change的连续相乘
        #period_stock_data['change'] = stock_data['change'].resample(period_type,how=lambda x:(x+1.0).prod()-1.0)
        #周线的open等于那一周中第一个交易日的open
        period_stock_data['open'] = stock_data['open'].resample(period_type).first()#,how='first')
        #周线的high等于那一周中的high的最大值
        period_stock_data['high'] = stock_data['high'].resample(period_type).max()#,how='max')
        #周线的low等于那一周中的low的最大值
        period_stock_data['low'] = stock_data['low'].resample(period_type).min()#,how='min')
        #周线的volume和money等于那一周中volume和money各自的和
        period_stock_data['volume'] = stock_data['volume'].resample(period_type).sum()#,how='sum')
        period_stock_data['amount'] = stock_data['amount'].resample(period_type).sum()#,how='sum')
        ##
        period_stock_data.dropna(axis=0, how='any', inplace=True)
        return  period_stock_data  
    
    #@jit
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
# 布林指标
   # @jit
    def bollinger(self,df,n):
        '''
        计算布林指标
        '''
        for i in range(len(df)):
            if i < n-1:
                continue
            df.ix[i, 'BOLL'] = df.close.values[i-n+1:i+1].mean()
            df.ix[i, 'UB'] = df.ix[i, 'BOLL'] + 2 * np.std(df.close.values[i-n+1:i+1], ddof=1)
            df.ix[i, 'LB'] = df.ix[i, 'BOLL'] - 2 * np.std(df.close.values[i-n+1:i+1], ddof=1)
        return df
import tushare as ts
class LHB_LT:
    '''
    获取龙虎榜数据和行业龙头
    '''
    def __init__(self):
        pass
    def getStockLHB(self,days =5):
        '''
        个股上榜统计
        输入：
            days：统计周期5、10、30和60日，默认为5日
        输出:
            code：代码
            name:名称
            count：上榜次数
            bamount：累积购买额(万)
            samount：累积卖出额(万)
            net：净额(万)
            bcount：买入席位数
            scount：卖出席位数
        '''
        df =ts.cap_tops(days)#5
        return df
import urllib.request as urllib2
import xlwt
from bs4 import BeautifulSoup 
# from html.parser import HTMLParser  
# from urllib import request
# from urllib import parse
# from urllib.request import urlopen
class hybg:
    def __init__(self):
        self.basePath ='./hyfx'
        self.pathExist(self.basePath)
    
    def getHydbFrom163(self,code):
        '''
        from 163 get  行业对比
        '''

        url_hydb_base ='http://quotes.money.163.com/f10/hydb_%s.html#01g02'
        url_hydb =url_hydb_base%(code)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url_hydb, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")

        #获取行业比对 标题
        itemAll = soup.findAll("h2",{"class":"title_01"})
        i =0
        retItem =[]
        while i < len(itemAll):
            retItem.append(itemAll[i].text)
            i =i+1
        ##获取行业比对 的所有表格
        tableAll = soup.findAll("table",{"class":"table_bg001 border_box table_sortable"})
        # print(len(tableAll))
        i =0
        retDf =[]
        while i < len(tableAll):
            table0 =tableAll[i]
            oneDf =pd.DataFrame()
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
                        # print(cells[j].text)
                        dfContent.append(cells[j].text)
                        j =j+1

                    dataContent.append(dfContent)
                   
            oneDf =pd.DataFrame(dataContent,columns=colName)
            
           
            retDf.append(oneDf)
            i= i+1
        return retItem,retDf #返回表格类别名称 和数据
    def pathExist(self,dirPath):
        '''
        检测路径是否存在 如果存在跳过，如果不存在生成
        '''
        if(os.path.exists(dirPath)==False):
            os.mkdir(dirPath)
            return True
        else:
            return True  
if __name__ == '__main__':
    source = 'D:\\new_tdx\\vipdoc\\sz\\lday'
    target = 'E:\\Project\\Stock\\testTdx'
    td =TdxData() 
    file_list = os.listdir(source)
    td.day2csv(source, 'sz002307.day', target)
    # for f in file_list:
    #     td.day2csv(source, f, target)
    # lhb =LHB()
    # lhb.getStockLHB()
    pass
