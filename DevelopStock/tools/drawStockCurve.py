import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import pandas as pd
def get_macd_data(data,short=0,long=0,mid=0):
    if short==0:
        short=12
    if long==0:
        long=26
    if mid==0:
        mid=9
    #计算短期的ema，使用pandas的ewm得到指数加权的方法，mean方法指定数据用于平均
    data['sema']=pd.Series(data['收盘价']).ewm(span=short).mean()
    #计算长期的ema，方式同上
    data['lema']=pd.Series(data['收盘价']).ewm(span=long).mean()
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
    # return data[['交易日期','data_dif','data_dea','data_macd']]
    return data

def cal_macd_system(data,short_,long_,m):
    '''
    data是包含高开低收成交量的标准dataframe
    short_,long_,m分别是macd的三个参数
    返回值是包含原始数据和diff,dea,macd三个列的dataframe
    '''
    data['diff']=data['收盘价'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
                data['收盘价'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
    data['dea']=data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
    data['macd']=2*(data['diff']-data['dea'])
    return data

zcfzb =pd.read_excel("000882.SZ.xls",'000882.SZ')
df0 = zcfzb[['交易日期',  '收盘价','成交量 （手）']]
df =df0
df['交易日期'] = pd.to_datetime(df['交易日期'],format="%Y%m%d")
df.set_index('交易日期',inplace=True)
# df['收盘价'].plot()
fig = plt.figure()
#close price
ax = fig.add_subplot(311)
ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
plt.xticks(pd.date_range(df.index[0],df.index[-1],freq='M'),rotation=45)
ax.plot(df.index,df['收盘价'],color='r')
plt.setp(ax.get_xticklabels(), fontsize=6,visible=False)
plt.grid(True)
#volume
ax1 = fig.add_subplot(312, sharex=ax)
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
plt.xticks(pd.date_range(df.index[0],df.index[-1],freq='M'),rotation=45)
# ax1.plot(df.index,df['收盘价'],color='r')
plt.bar(df.index,df['成交量 （手）'].values,width = 0.2,color='g',label="2nd")  # 直方图的画法
plt.setp(ax1.get_xticklabels())
plt.grid(True)
#macd
kk =get_macd_data(df0)
# kk =cal_macd_system(df0,12,26,9)

# kk['交易日期'] = pd.to_datetime(kk['交易日期'],format="%Y%m%d")
# kk.set_index('交易日期',inplace=True)

ax1 = fig.add_subplot(313, sharex=ax)
ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y%m%d'))
plt.xticks(pd.date_range(kk.index[0],kk.index[-1],freq='M'),rotation=45)
# ax1.plot(df.index,df['收盘价'],color='r')
plt.bar(df.index,kk['data_macd'].values,width = 0.2,color='g',label="2nd")  # 直方图的画法
plt.setp(ax1.get_xticklabels())
plt.grid(True)
plt.show()




