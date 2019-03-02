# from matplotlib.pylab import date2num
# import matplotlib.pyplot as plt 
# import datetime
# import numpy as np
# import pandas as pd
# import matplotlib.finance as mpf
# hist_data =pd.read_excel("000882.SZ.xls",'000882.SZ') 
# # 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
# data_list = []
# for dates,row in hist_data.iterrows():
#     # 将时间转换为数字
#     date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
#     t = date2num(date_time)
#     open,high,low,close = row[:4]
#     datas = (t,open,high,low,close)
#     data_list.append(datas)
 
# # 创建子图
# fig, ax = plt.subplots()
# fig.subplots_adjust(bottom=0.2)
# # 设置X轴刻度为日期时间
# ax.xaxis_date()
# plt.xticks(rotation=45)
# plt.yticks()
# plt.title("股票代码：601558两年K线图")
# plt.xlabel("时间")
# plt.ylabel("股价（元）")
# mpf.candlestick_ohlc(ax,data_list,width=1.5,colorup='r',colordown='green')
# plt.grid()


# import pandas as pd
# from pandas import DataFrame
# import matplotlib.pyplot as plt
# import matplotlib.dates as dates
# import mpl_finance as mpf
# from matplotlib.ticker import Formatter
# import numpy as np
# a =np.array([1,2,3])
# b =np.array([2,1,4])
# print(a>b)

# # dfcvs = DataFrame([
# #     ["2018/09/17-21:34", 3646, 3650,3644,3650],
# #     ["2018/09/17-21:35", 3650, 3650,3648,3648],
# #     ["2018/09/17-21:36", 3650, 3650,3648,3650],
# #     ["2018/09/17-21:37", 3652, 3654,3648,3652]
# # ])
# dfcvs = DataFrame([
#     ["2018/09/17", 3646, 3650,3644,3650],
#     ["2018/09/18", 3650, 3650,3648,3648],
#     ["2018/09/19", 3650, 3650,3648,3650],
#     ["2018/09/21", 3652, 3654,3648,3652]
# ])
# dfcvs.columns = ['时间','开盘','最高','最低','收盘']
# # dfcvs['时间']=pd.to_datetime(dfcvs['时间'],format="%Y/%m/%d-%H:%M")
# dfcvs['时间']=pd.to_datetime(dfcvs['时间'],format="%Y/%m/%d")
# #matplotlib的date2num将日期转换为浮点数，整数部分区分日期，小数区分小时和分钟
# #因为小数太小了，需要将小时和分钟变成整数，需要乘以24（小时）×60（分钟）=1440，这样小时和分钟也能成为整数
# #这样就可以一分钟就占一个位置

 

# dfcvs['时间']=dfcvs['时间'].apply(lambda x:dates.date2num(x)*1440)
# data_mat=dfcvs.as_matrix()
    
# fig,ax=plt.subplots(figsize=(1200/72,480/72))
 
# fig.subplots_adjust(bottom=0.1)   
# mpf.candlestick_ohlc(ax,data_mat,colordown='#53c156', colorup='#ff1717',width=200,alpha=1)

# #将x轴的浮点数格式化成日期小时分钟
# #默认的x轴格式化是日期被dates.date2num之后的浮点数，因为在上面乘以了1440，所以默认是错误的
# #只能自己将浮点数格式化为日期时间分钟
# #参考https://matplotlib.org/examples/pylab_examples/date_index_formatter.html
# class MyFormatter(Formatter):
#             def __init__(self, dates, fmt='%Y%m%d %H:%M'):
#                 self.dates = dates
#                 self.fmt = fmt
    
#             def __call__(self, x, pos=0):
#                 'Return the label for time x at position pos'
#                 ind = int(np.round(x))
#                 #ind就是x轴的刻度数值，不是日期的下标

#                 return dates.num2date( ind/1440).strftime(self.fmt)
        
# formatter = MyFormatter(data_mat[:,0],'%Y%m%d')
# ax.xaxis.set_major_formatter(formatter)

# for label in ax.get_xticklabels():
#             label.set_rotation(90)
#             label.set_horizontalalignment('right')
           
# plt.show()




import matplotlib.pyplot as plt 
import mpl_finance as mpf
import numpy as np 
import pandas as pd 
from matplotlib.pylab import date2num 
import matplotlib.ticker as ticker 
import time 
# data=pd.read_csv(u'assets/兴业银行.csv',usecols=['date','open','close','high','low','volume']) 
zcfzb =pd.read_excel("000882.SZ.xls",'000882.SZ')
# df_raw = zcfzb[['交易日期',  '开盘价','最高价','最低价','收盘价','成交量 （手）']]
data =pd.DataFrame()
data['date'] =zcfzb['交易日期']
data['open']=zcfzb['开盘价']
data['high']=zcfzb['最高价']
data['low']=zcfzb['最低价']
data['close']=zcfzb['收盘价']
data['volume']=zcfzb['成交量 （手）']
data[data['volume']==0]=np.nan 
data=data.dropna() 
data.sort_values(by='date',ascending=True,inplace=True) 
# 原始的csv 读入进来 DataFrame 的 columns 顺序不符合candlestick_ochl 要求的顺序 
# columns 的顺序一定是 date, open, close, high, low, volume
# 这样才符合 candlestick_ochl 绘图要求的数据结构 
# 下面这个是改变列顺序最优雅的方法 
data=data[['date','open','close','high','low','volume']] 
data=data.head(62) 
# 生成横轴的刻度名字 
date_tickers=data.date.values 
weekday_quotes=[tuple([i]+list(quote[1:])) for i,quote in enumerate(data.values)] 
print (weekday_quotes) 
fig,ax=plt.subplots(figsize=(1200/72,480/72)) 
def format_date(x,pos=None): 
    if x<0 or x>len(date_tickers)-1: 
        return '' 
    return date_tickers[int(x)] 
ax.xaxis.set_major_locator(ticker.MultipleLocator(6)) 
ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date)) 
ax.grid(True)
 # fig.autofmt_xdate() 
mpf.candlestick_ochl(ax,weekday_quotes,colordown='#53c156', colorup='#ff1717',width=0.2) 
plt.show() 
