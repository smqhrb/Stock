############################################
#   QT 批量处理通达信二进制数据 进入 数据库 
#   计算均线 布林 MACD  均线斜率 均线粘合的  日 周 月 的 计算方法 
#   PY计算出来的结果 和通达信的 
#   PY  能否先 做个挑选和行业 和板块 的龙头股 结合龙虎榜 经常上榜的股票
#
#############################################
# 　一、通达信的股票文件格式
# 　　通过交易软件的“盘后数据下载”功能，可以下载到所有股票的日线数据，具体位置在：
# 　　交易软件的安装目录\vipdoc\sh[sz]\lday
# 　　文件命名为：sh[sz]000001.day
# 　　日线文件中，每32字节（32bytes）为一天的记录。
# 　　每4个字节为一项数据：
# 　　第1项，交易日期
#   　第2项，开盘价
# 　　第3项，最高价
# 　　第4项，最低价
# 　　第5项，收盘价
# 　　第6项，成交金额
# 　　第7项，成交量
# 　　第8项，未使用
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from struct import unpack
 
 
# 将通达信的日线文件转换成CSV格式

def day2csv(source_dir, file_name, target_dir):
    # 以二进制方式打开源文件
    source_file = open(source_dir + os.sep + file_name, 'rb')
    buf = source_file.read()
    source_file.close()
 
    # 打开目标文件，后缀名为CSV
    target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
    buf_size = len(buf)
    rec_count = int(buf_size / 32)
    begin = 0
    end = 32
    header = str('date') + ', ' + str('open') + ', ' + str('high') + ', ' + str('low') + ', ' \
        + str('close') + ', ' + str('amount') + ', ' + str('vol') + ', ' + str('str07') + '\n'
    target_file.write(header)
    for i in range(rec_count):
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
        a = unpack('IIIIIfII', buf[begin:end])
        line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
            + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
            + str(a[6]) + ', ' + str(a[7]) + ', ' + '\n'
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()
# source = 'D:/new_tdx/vipdoc/sz/lday/'
# target = 'E:/Project/Stock/testTdx/'

# file_list = os.listdir(source)
# for f in file_list:
#     day2csv(source, f, target)

# 将通达信的分时文件文件转换成CSV格式
# 通达信5分钟线*.lc5文件和*.lc1文件
#     文件名即股票代码
#     每32个字节为一个5分钟数据，每字段内低字节在前
#     00 ~ 01 字节：日期，整型，设其值为#         # 将字节流转换成Python数据格式
#         # I: unsigned int
#         # f: float
#         a = unpack('IIIIIfII', buf[begin:end])
#         line = str(a[0]) + ', ' + str(a[1] / 100.0) + ', ' + str(a[2] / 100.0) + ', ' \
#             + str(a[3] / 100.0) + ', ' + str(a[4] / 100.0) + ', ' + str(a[5] / 10.0) + ', ' \
#             + str(a[6]) + ', ' + str(a[7]) + ', ' + '\n'
#         target_file.write(line)
#         begin += 32
#         end += 32
#     target_file.close()
#                 num，则日期计算方法为：
#                   year=floor(num/2048)+2004;
#                   month=floor(mod(num,2048)/100);
#                   day=mod(mod(num,2048),100);
#     02 ~ 03 字节： 从0点开始至目前的分钟数，整型
#     04 ~ 07 字节：开盘价，float型             
#     08 ~ 11 字节：最高价，float型
#     12 ~ 15 字节：最低价，float型
#     16 ~ 19 字节：收盘价，float型
#     20 ~ 23 字节：成交额，float型
#     24 ~ 27 字节：成交量（股），整型
#     28 ~ 31 字节：（保留）

def fz2csv(source_dir, file_name, target_dir):
    source_file = open(source_dir + os.sep + file_name, 'rb')
    buf = source_file.read()
    source_file.close()
    target_file = open(target_dir + os.sep + file_name + '.csv', 'w')
    buf_size = len(buf)
    rec_count = int(buf_size / 32)
    begin = 0
    end = 32
    header = str('Date') + ', '+str('Time') +',' \
        + str('open') + ', ' + str('low') + ', ' + str('high') + ', ' + str('close') +', ' + str('amount') +', ' + str('vol')+ '\n'
    target_file.write(header)
    for i in range(rec_count):
        # 将字节流转换成Python数据格式
        # I: unsigned int
        # f: float
#                   year=floor(num/2048)+2004;
#                   month=floor(mod(num,2048)/100);
#                   day=mod(mod(num,2048),100);
#     02 ~ 03 字节： 从0点开始至目前的分钟数，整型
        a = unpack('hhfffffii', buf[begin:end])
        line = str(int(a[0]/2048)+2004) + '-' + str(int((a[0] % 2048)/100)) + '-' + str(int((a[0] % 2048)%100))+ ','+ str(int(a[1] / 60)) + ':' \
            + str(a[1] % 100) + ', ' + str(a[2]) + ', ' + str(a[3]) + ', ' \
            + str(a[4]) + ', ' + str(a[5]) +  ', ' + str(a[6]) +  ', ' + str(a[7])+ '\n'
        target_file.write(line)
        begin += 32
        end += 32
    target_file.close()

# source = 'D:/new_tdx/vipdoc/sz/fzline/'
# target = 'E:/Project/Stock/testTdx/'
# file_list = os.listdir(source)
# for f in file_list:
#     fz2csv(source, f, target)

source = 'D:/new_tdx/vipdoc/sz/minline/'
target = 'E:/Project/Stock/testTdx/'
file_list = os.listdir(source)
for f in file_list:
    fz2csv(source, f, target)




import os

import pandas as pd

stock_data = pd.read_csv('stock data/sh600898.csv',parse_dates=[1])

#设定转换周期period_type  转换为周是'W',月'M',季度线'Q',五分钟'5min',12天'12D'
period_type = 'W'
#将[date]设定为    index   inplace是原地修改，不要创建一个新对象
stock_data.set_index('date',inplace=True)
#进行转换，周线的每个变量都等于那一周中最后一个交易日的变量值
period_stock_data = stock_data.resample(period_type,how='last')
#周线的change等于那一周中每日change的连续相乘
period_stock_data['change'] = stock_data['change'].resample(period_type,how=lambda x:(x+1.0).prod()-1.0)
#周线的open等于那一周中第一个交易日的open
period_stock_data['open'] = stock_data['open'].resample(period_type,how='first')
#周线的high等于那一周中的high的最大值
period_stock_data['high'] = stock_data['high'].resample(period_type,how='max')
#周线的low等于那一周中的low的最大值
period_stock_data['low'] = stock_data['low'].resample(period_type,how='min')
#周线的volume和money等于那一周中volume和money各自的和
period_stock_data['volume'] = stock_data['volume'].resample(period_type,how='sum')
period_stock_data['money'] = stock_data['money'].resample(period_type,how='sum')
#计算周线turnover
period_stock_data['turnover'] = period_stock_data['volume']/\
                                (period_stock_data['traded_market_value']/period_stock_data['close'])
#股票在有些周一天都没有交易，将这些周去除
period_stock_data = period_stock_data[period_stock_data['code'].notnull()]
period_stock_data.reset_index(inplace=True)
#导出数据
period_stock_data.to_csv('week_stock_data.csv',index=False)