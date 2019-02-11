
'''
get stock data
refresh the data as you want. 
'''
import tushare as ts
import datetime
from datetime import timedelta
import numpy as np
import math
import os
# import Config.configureStock as cf
import pandas as pd
class stockData():
    def __init__(self,code,start,end):
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
        self.pro = ts.pro_api()
        self.startTime =start
        self.endTime =end
        self.code =code

    def preDataForProcess(self):
        '''
        predict few days close price.
        '''
        # start = datetime.datetime(2019, 1, 7)
        # end = datetime.datetime(2019, 1, 9)
        #从互联网获取数据
        # df1 = self.pro.daily(ts_code=self.code, start_date=self.startTime, end_date=self.endTime)
        df1 = self.pro.weekly(ts_code=self.code, start_date=self.startTime, end_date=self.endTime, fields='ts_code,trade_date,open,high,low,close,vol,amount')

        df=df1.sort_values(by=['trade_date'])

        print(df.head())
        df = df[['open',  'high',  'low',  'close', 'vol']]
        df['HL_PCT'] = (df['high'] - df['low']) / df['close'] * 100.0
        df['PCT_change'] = (df['close'] - df['open']) / df['open'] * 100.0
        df = df[['close', 'HL_PCT', 'PCT_change', 'vol']]
        print(df)
        #print(df.head())
        forecast_col = 'close'
        df.fillna(value=-99999, inplace=True)
        forecast_out = 1#int(math.ceil(0.01 * len(df)))
        #预测forecast_out天后的

        df['label'] = df[forecast_col].shift(-forecast_out)

        print(df)
        print(df.shape)
        print(df.tail())
        X = np.array(df.drop(['label'], 1))
        # X = preprocessing.scale(X)
        X = X[:-forecast_out]
        df.dropna(inplace=True)
        y = np.array(df['label'])
        return X,y
    def preDataForCluster(self):
        '''
        1. get stock HS300
        2. prepare weekly data as 'open close high vol'
        '''
        if(os.path.isfile("HS300Data.xls")):
            hs300Data =pd.read_excel("HS300Data.xls")
            hs300 =pd.read_excel('hs300.xls')
            for code in hs300['code']:
                if(code <600000):
                    codeStr="%06d.SZ"%(code)
                else:
                    codeStr="%06d.SH"%(code)
                print(hs300Data.ix[hs300Data['ts_code']==codeStr])
           
           

        else:
            dfH =pd.DataFrame()
            # hs300 =pd.read_excel(cf.HS300)
            hs300 =pd.read_excel('hs300.xls')
            for code in hs300['code']:
                if(code <600000):
                    codeStr="%06d.SZ"%(code)
                else:
                    codeStr="%06d.SH"%(code)
                df = self.pro.weekly(ts_code=codeStr, start_date=self.startTime, end_date=self.endTime, fields='ts_code,trade_date,open,high,low,close,vol,amount')
                dfH =dfH.append(df)
            # print(dfH)
            writer = pd.ExcelWriter('HS300Data.xls')
            df=dfH.sort_values(by=['ts_code'])
            df.to_excel(writer,sheet_name='HS300Data')   
            writer.save()

if __name__ == '__main__':
    # now_time = datetime.datetime.now()
    # end =now_time.strftime('%Y%m%d')
    # lastyear_time =now_time -timedelta(days=365)
    # start =lastyear_time.strftime('%Y%m%d')    
    # sd =stockData('000651.SZ',start,end)
    # X,y =sd.preDataForProcess()
    # print(X,y)
    # print(X.shape)
    # print(y.shape)

    sd =stockData('000651.SZ','20180101','20190101')
    sd.preDataForCluster()

