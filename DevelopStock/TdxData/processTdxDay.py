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
        pass
    def day2csv(self,source_dir, file_name, target_dir):
        '''
        获取输入级从通达信的日线数据
        日线数据位于：new_tdx/vipdoc/sz/lday/,new_tdx/vipdoc/sh/lday/
        '''
        # 以二进制方式打开源文件
        source_file = open(source_dir + os.sep + file_name, 'rb')
        buf = source_file.read()
        source_file.close()
    
        # 打开目标文件，后缀名为CSV
        #target_file = open(target_dir + os.sep + file_name + '.xls', 'wb+')
        target_file = target_dir + os.sep + file_name + '.xls'
        buf_size = len(buf)
        rec_count = int(buf_size / 32)
        begin = 0
        end = 32
        # header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
        #     + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('str07') + '\n'
        #target_file.write(header)
# 　　第1项，交易日期
#   　第2项，开盘价
# 　　第3项，最高价
# 　　第4项，最低价
# 　　第5项，收盘价
# 　　第6项，成交金额
# 　　第7项，成交量
# 　　第8项，未使用
        dayTrade =[]
        
        for i in range(rec_count):
            # 将字节流转换成Python数据格式
            # I: unsigned int
            # f: float
            a = unpack('IIIIIfII', buf[begin:end])
            # line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
            #     + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
            #     + str(a[6]) + ', ' + str(a[7]) + ', ' + '\n'
            date =str(a[0]) 
            date_time = datetime.datetime.strptime(date,'%Y%m%d')
            date= date_time.strftime('%Y-%m-%d')
            openPrice =(a[1] / 100.0)
            highPrice =(a[2] / 100.0)
            lowPrice =(a[3] / 100.0)
            closePrice =(a[4] / 100.0)
            amount =(a[5] / 10.0)
            volume =(a[6])

            dayTrade.append([date,openPrice,highPrice,lowPrice,closePrice,amount,volume])
           # target_file.write(line)
            begin += 32
            end += 32
        dayTdx =pd.DataFrame(dayTrade)
        #   jbxx.to_excel(write,sheet_name='基本指标(元)',index=True)
        dayTdx.rename(columns={0:'date',1:'open',2:'high',3:'low',4:'close',5:'amount',6:'volume'},inplace=True)#
        #dayTdx.set_index('date',inplace=True)
        dayTdx.sort_values('date', ascending=False, inplace=True)
        dayTdx.set_index(pd.DatetimeIndex(pd.to_datetime(dayTdx.date)), inplace=True)
        # # 周数据
        weekTdx =self.periodChange(dayTdx,'W')
        # 月数据
        monthTdx =self.periodChange(dayTdx,'M')
        #计算均线 布林 MACD  均线斜率 均线粘合

        write = pd.ExcelWriter(target_file)
        # 将数据按照交易日期从近到远排序
       
        # ========== 将算好的数据输出到xls文件 - 注意：这里请填写输出文件在您电脑中的路径
        dayTdx =self.indicatorCalc(dayTdx)
        weekTdx =self.indicatorCalc(weekTdx)
        monthTdx =self.indicatorCalc(monthTdx)
        
        dayTdx.to_excel(write,sheet_name=file_name)
        weekTdx.to_excel(write,sheet_name='周')
        monthTdx.to_excel(write,sheet_name='月')
        write.save()

    def indicatorCalc(self,stock_data):
        '''
        计算指数 MACD MA 三线粘合 斜率
        '''
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
        #布林线
        self.bollinger(stock_data,20)
        return stock_data
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
        return  period_stock_data  

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
    def bollinger(self,df,n):
        for i in range(len(df)):
            if i < n-1:
                continue
            df.ix[i, 'BOLL'] = df.close.values[i-n+1:i+1].mean()
            df.ix[i, 'UB'] = df.ix[i, 'BOLL'] + 2 * np.std(df.close.values[i-n+1:i+1], ddof=1)
            df.ix[i, 'LB'] = df.ix[i, 'BOLL'] - 2 * np.std(df.close.values[i-n+1:i+1], ddof=1)
        return df
import tushare as ts
class LHB:
    '''
    获取龙虎榜数据
    '''
    def __init__(self):
        pass
    def getStockLHB(self):
        df =ts.cap_tops()
        print(df)
# code：代码
# name:名称
# count：上榜次数
# bamount：累积购买额(万)
# samount：累积卖出额(万)
# net：净额(万)
# bcount：买入席位数
# scount：卖出席位数
    # def urlOpenContent(self,urlBase,urlfix=""):
    #     '''
    #     parameter:
    #         url is made by urlBase urlfix
    #     return content
    #     '''
    #     url =urlBase
    #     headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
    #     req = urllib2.Request(url, headers = headers)
    #     try:
    #         content = urllib2.urlopen(req).read()
    #     except:
    #         return 
    #     return content
    # def getStockLHB(self):
    #     '''
    #     获取流动股本信息
    #     http://data.eastmoney.com/stock/stockstatistic.html
    #     '''

    #     # stockGbbd ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCI_StockStructure/stockid/000001.phtml'#股本变动
    #     emLHB ='http://data.eastmoney.com/stock/stockstatistic.html'#股本变动
    #     content =self.urlOpenContent(emLHB)
    #     soup = BeautifulSoup(content,features="lxml")
    #     table = soup.find("table",{"id":"tab-1"})
    #     tbody =table.find("tbody")
    #     tr =tbody.findAll("tr")
    #     i=0
    #     while(i<len(tr)):
    #         td = tr[i].findAll("td")
    #         if(len(td)>0):
    #             ind =td[0].text
    #         i =i+1
            


        

if __name__ == '__main__':
    # source = 'D:\\new_tdx\\vipdoc\\sz\\lday\\'
    # target = 'E:\\Project\\Stock\\testTdx'
    # td =TdxData() 
    # file_list = os.listdir(source)
    # for f in file_list:
    #     td.day2csv(source, f, target)
    lhb =LHB()
    lhb.getStockLHB()
