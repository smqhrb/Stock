


# import pandas as pd

# import tushare as ts

# #定义一个函数get_a_share

# def get_a_share(code):

#     #使用tushare的get_k_data调用A股股票数据

#     data = ts.get_k_data(code)

#     #删除列code

#     data = data.drop('code',axis = 1)

#     #返回修改后的股票数据

#     return data

# #定义函数，获取macd,导入数据，初始化三个参数

# def get_macd_data(data,short=0,long=0,mid=0):
#     if short==0:
#         short=12
#     if long==0:
#         long=26
#     if mid==0:
#         mid=9
#     #计算短期的ema，使用pandas的ewm得到指数加权的方法，mean方法指定数据用于平均
#     data['sema']=pd.Series(data['close']).ewm(span=short).mean()
#     #计算长期的ema，方式同上
#     data['lema']=pd.Series(data['close']).ewm(span=long).mean()
#     #填充为na的数据
#     data.fillna(0,inplace=True)
#     #计算dif，加入新列data_dif
#     data['data_dif']=data['sema']-data['lema']
#     #计算dea
#     data['data_dea']=pd.Series(data['data_dif']).ewm(span=mid).mean()
#     #计算macd
#     data['data_macd']=2*(data['data_dif']-data['data_dea'])
#     #填充为na的数据
#     data.fillna(0,inplace=True)
#     #返回data的三个新列
#     return data[['date','data_dif','data_dea','data_macd']]
# #请输入A股股票代码
# code = str(input('输入A股股票代码:'))
# data = get_a_share(code)
# macd = get_macd_data(data)
# ###################
# def cal_macd_system(data,short_,long_,m):
#     '''
#     data是包含高开低收成交量的标准dataframe
#     short_,long_,m分别是macd的三个参数
#     返回值是包含原始数据和diff,dea,macd三个列的dataframe
#     '''
#     data['diff']=data['close'].ewm(adjust=False,alpha=2/(short_+1),ignore_na=True).mean()-\
#                 data['close'].ewm(adjust=False,alpha=2/(long_+1),ignore_na=True).mean()
#     data['dea']=data['diff'].ewm(adjust=False,alpha=2/(m+1),ignore_na=True).mean()
#     data['macd']=2*(data['diff']-data['dea'])
#     return data
# ###################
# import pandas as pd
# import numpy as np
# import datetime
# import time
# #获取数据
# df=pd.read_csv('C:/Users/HXWD/Desktop/000001.csv',encoding='gbk')
# df.columns=['date','code','name','close','high','low','open','preclose',
# 'change','change_per','volume','amt']
# df=df[['date','open','high','low','close','volume','amt']]
# df.head()
# def get_EMA(df,N):
#     for i in range(len(df)):
#         if i==0:
#             df.ix[i,'ema']=df.ix[i,'close']
#         if i>0:
#             df.ix[i,'ema']=(2*df.ix[i,'close']+(N-1)*df.ix[i-1,'ema'])/(N+1)
#     ema=list(df['ema'])
#     return ema
# def get_MACD(df,short=12,long=26,M=9):
#     a=get_EMA(df,short)
#     b=get_EMA(df,long)
#     df['diff']=pd.Series(a)-pd.Series(b)
#     #print(df['diff'])
#     for i in range(len(df)):
#         if i==0:
#             df.ix[i,'dea']=df.ix[i,'diff']
#         if i>0:
#             df.ix[i,'dea']=(2*df.ix[i,'diff']+(M-1)*df.ix[i-1,'dea'])/(M+1)
#     df['macd']=2*(df['diff']-df['dea'])
#     return df
# get_MACD(df,12,26,9)



 
#########################
'''


    12日EMA的计算：EMA12 = 前一日EMA12 X 11/13 + 今日收盘 X 2/13
    26日EMA的计算：EMA26 = 前一日EMA26 X 25/27 + 今日收盘 X 2/27
    差离值（DIF）的计算： DIF = EMA12 - EMA26，即为talib-MACD返回值macd
    根据差离值计算其9日的EMA，即离差平均值，是所求的DEA值。今日DEA = （前一日DEA X 8/10 + 今日DIF X 2/10），即为talib-MACD返回值signal
    DIF与它自己的移动平均之间差距的大小一般BAR=（DIF-DEA)x2，即为MACD柱状图。

'''
import pandas as pd
import numpy as np
# ema=data['close'].ewm(span=12).mean()

def get_macd_data(df_raw,fast_period=12,slow_period=26,signal_period=9): 
    # df_raw['close'] -- 收盘价 
    # 收盘价按照日期升序( df_raw['date'] )排列 
    # 返回值都是 Series 
    fast_ewm=df_raw['收盘价'].ewm(span=fast_period).mean() 
    slow_ewm=df_raw['收盘价'].ewm(span=slow_period).mean() 
    dif=fast_ewm-slow_ewm 
    dea=dif.ewm(span=signal_period).mean() 
    # 一般概念里，macd柱是 (dif-dea)*2，实际上只是为了扩大显示效果 
    # # 实测后发现，也可以不乘以2，效果也足够清楚了 
    bar=(dif-dea)*2 
    # 将bar 分成红绿柱分别导出数据， 
    # #目的是后续用matplotlib绘图时，能够分色绘制 
    red_bar=bar[bar>=0] 
    green_bar=bar[bar<0] 
    return dif,dea,red_bar,green_bar
import matplotlib as mpl 
from matplotlib.font_manager import FontProperties 
import matplotlib.pyplot as plt 
title_font=FontProperties(family='YouYuan',size=18) 
mpl.rcParams['axes.unicode_minus']=False 
def draw_macd(df_raw, dif, dea, red_bar, green_bar, canvas_w=1000, canvas_h=480, xtick_period=20, title=u'MACD'): 
    '''
    •df_raw - 原始的从 csv 导出数据后生成的DataFrame，目的是用在生成major_xticks时定位使用
    •dif, dea, red_bar, green_bar 是使用 get_macd_data 方法计算出的MACD指标
    •canvas_w, canvas_h 为期望绘制出的图形宽度和高度，单位是像素
    •xtick_period 为生成x 方向刻度时，每间隔多少个数值，取一个值作为刻度显示出来——如果将全部日期显示出来，x方向的刻度将会是密密麻麻一片黑
    •title 是图形的标题
    '''
    dpi=72 
    figsize=canvas_w/72,canvas_h/72 
    plt.figure(figsize=figsize) 
    p_dif=plt.plot(dif.index,dif.values) 
    p_dea=plt.plot(dea.index,dea.values) 
    plt.bar(red_bar.index, red_bar.values, color='#d62728') 
    plt.bar(green_bar.index, green_bar.values, color='#889966') 
    major_index=df_raw.index[df_raw.index%xtick_period==0] 
    major_xtics=df_raw['交易日期'][df_raw.index%xtick_period==0] 
    plt.xticks(major_index,major_xtics) 
    plt.legend((p_dif[0],p_dea[0]),[u'DIF',u'DEA']) 
    plt.title(title,fontproperties=title_font) 
    plt.show() 


zcfzb =pd.read_excel("000882.SZ.xls",'000882.SZ')
df_raw = zcfzb[['交易日期',  '收盘价','成交量 （手）']]
# df_raw=pd.read_csv(u'assets/招商银行.csv',usecols=['close','date','volume']) 
# 注意要排除无交易的单日数据 
df_raw[df_raw['成交量 （手）']==0]=np.nan 
df_raw.dropna() 
df_raw.sort_values(by='交易日期',ascending=True,inplace=True) 
# 注意，df_raw.index 必须是升序 
# 如果由于对 date 排序后，index变成了降序
# 要单独把index的顺序反过来 
df_raw.index=df_raw.index[::-1] 
dif,dea,red_bar,green_bar=get_macd_data(df_raw) 
draw_macd(df_raw=df_raw, dif=dif, dea=dea, 
            red_bar=red_bar, green_bar=green_bar, xtick_period=25, title=u'招商银行 MACD') 


########################
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
