


import pandas as pd

import tushare as ts

#定义一个函数get_a_share

def get_a_share(code):

    #使用tushare的get_k_data调用A股股票数据

    data = ts.get_k_data(code)

    #删除列code

    data = data.drop('code',axis = 1)

    #返回修改后的股票数据

    return data

#定义函数，获取macd,导入数据，初始化三个参数

def get_macd_data(data,short=0,long=0,mid=0):
    if short==0:
        short=12
    if long==0:
        long=26
    if mid==0:
        mid=9
    #计算短期的ema，使用pandas的ewm得到指数加权的方法，mean方法指定数据用于平均
    data['sema']=pd.Series(data['close']).ewm(span=short).mean()
    #计算长期的ema，方式同上
    data['lema']=pd.Series(data['close']).ewm(span=long).mean()
    #填充为na的数据
    data.fillna(0,inplace=True)
    #计算dif，加入新列data_dif
    data['data_dif']=data['sema']-data['lema']
    #计算dea
    data['data_dea']=pd.Series(data['data_dif']).ewm(span=mid).mean()
    #计算macd
    data['data_macd']=2*(data['data_dif']-data['data_dea'])
    #填充为na的数据
    data.fillna(0,inplace=True)
    #返回data的三个新列
    return data[['date','data_dif','data_dea','data_macd']]
#请输入A股股票代码
code = str(input('输入A股股票代码:'))
data = get_a_share(code)
macd = get_macd_data(data)
###################
def cal_macd_system(data,short_,long_,m):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['diff']=data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    data['dea']=data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    data['macd']=2*(data['diff']-data['dea'])
    return data
###################
import pandas as pd
import numpy as np
import datetime
import time
#获取数据
df=pd.read_csv('C:/Users/HXWD/Desktop/000001.csv',encoding='gbk')
df.columns=['date','code','name','close','high','low','open','preclose',
'change','change_per','volume','amt']
df=df[['date','open','high','low','close','volume','amt']]
df.head()
def get_EMA(df,N):
    for i in range(len(df)):
        if i==0:
            df.ix[i,'ema']=df.ix[i,'close']
        if i>0:
            df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)
    ema=list(df['ema'])
    return ema
def get_MACD(df,short=12,long=26,M=9):
    a=get_EMA(df,short)
    b=get_EMA(df,long)
    df['diff']=pd.Series(a)-pd.Series(b)
    #print(df['diff'])
    for i in range(len(df)):
        if i==0:
            df.ix[i,'dea']=df.ix[i,'diff']
        if i>0:
            df.ix[i,'dea']=(2*df.ix[i,'diff']+(M-1)*df.ix[i-1,'dea'])/(M+1)
    df['macd']=2*(df['diff']-df['dea'])
    return df
get_MACD(df,12,26,9)
df