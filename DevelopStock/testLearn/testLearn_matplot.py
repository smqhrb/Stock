import matplotlib.pyplot as plt

# def PlotDemo1():
#     fig  = plt.figure()
#     fig.suptitle('figure title demo', fontsize = 14, fontweight='bold')
#     ax = fig.add_subplot(2,1,1)
#     ax.set_title("axes title")
#     ax.set_xlabel("x label")      
#     ax.set_ylabel("y label")
#     ax.plot([1,2,3,4],[2,3,4,5])
#     ax = fig.add_subplot(2,1,2)
#     ax.plot([2,3,4,5],[1,2,3,4])
#     plt.show()
# if __name__ == '__main__':
#     PlotDemo1()

import matplotlib.pyplot as plt
import numpy as np

# t = np.arange(0.01, 5.0, 0.01)
# s1 = np.sin(2*np.pi*t)
# s2 = np.exp(-t)
# s3 = np.sin(4*np.pi*t)

# ax1 = plt.subplot(311)
# plt.plot(t, s1)
# plt.setp(ax1.get_xticklabels(), fontsize=6)

# # share x only
# ax2 = plt.subplot(312, sharex=ax1)
# plt.plot(t, s2)
# # make these tick labels invisible
# plt.setp(ax2.get_xticklabels(), visible=False)

# # share x and y
# ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
# plt.plot(t, s3)
# plt.xlim(0.01, 5.0)
# plt.show()
import numpy as np
import matplotlib.pyplot as plt

# plt.axis([0, 100, 0, 1])
# plt.ion()

# xs = [0, 0]
# ys = [1, 1]

# for i in range(100):
#     y = np.random.random()
#     xs[0] = xs[1]
#     ys[0] = ys[1]
#     xs[1] = i
#     ys[1] = y
#     plt.plot(xs, ys)
#     plt.pause(0.1)
# plt.show()	

fr = pd.Series(va.values.cumsum() / va.values.sum())
va.plot(kind='bar')
fr.plot(color='r',secondary_y=True, style='-o')
plt.annotate(format(fr[7], '.2%'), xy=(7, fr[7]), xytext=(7*0.9, fr[7]*0.9),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))  # 用于注释图形指标
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
# plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# plt1 = plt.pie(va.values,
#                labels=va.index,
#                autopct='%1.1f%%')
plt.xticks(rotation=50)  # 设置字体大小和字体倾斜度
plt.show()

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
y1 = []
for i in range(50):
    y1.append(i)  # 每迭代一次，将i放入y1中画出来
    ax.cla()   # 清除键
    ax.bar(y1, label='test', height=y1, width=0.3)
    ax.legend()
    plt.pause(0.1)
plt.show()					


# plt.figure(figsize=(7,5))       # 确定图片大小

# plt.subplot(211)                # 确定第一个图的位置
# plt.plot(df.index,df['收盘价'].values,'b',label="1st")
# plt.grid(True)
# plt.axis('tight')
# plt.ylabel('Values',size=20)
# plt.title("000012")

# plt.legend(loc=0)

# plt.subplot(212)               # 确定第2个图的位置
# plt.bar(df.index,df['成交量 （手）'].values,width = 0.2,color='g',label="2nd")  # 直方图的画法
# plt.grid(True)
# plt.xlabel("Time",size=20)
# plt.ylabel("Volume",size=20)
# plt.legend(loc=0)
# # plt.gcf().autofmt_xdate()
# plt.show()


# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
stock_data = pd.read_csv('stock data/sh600000.csv', parse_dates=[1])


 # 将数据按照交易日期从远到近排序
stock_data.sort('date', inplace=True)




 # ========== 计算移动平均线


# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]


 # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for ma in ma_list:
     stock_data['MA_' + str(ma)] = pd.rolling_mean(stock_data['close'], ma)


 # 计算指数平滑移动平均线EMA
 for ma in ma_list:
     stock_data['EMA_' + str(ma)] = pd.ewma(stock_data['close'], span=ma)


 # 将数据按照交易日期从近到远排序
stock_data.sort('date', ascending=False, inplace=True)


 # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
stock_data.to_csv('sh600000_ma_ema.csv', index=False)