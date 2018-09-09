import urllib3
import tushare as ts
import pandas as pd
import sys
sys.path.append('E:\\Project\\Stock\DevelopStock\\')
# sys.path.append('../UI')
# import UI
from Config import dbOperate
# import pymysql
# pymysql.install_as_MySQLdb()
# sys.path.append(r'..\UI')
# from sqlalchemy import create_engine
# import tushare as ts
# df = ts.get_hist_data('600848')
# engine = create_engine('mysql://root:smq1234@127.0.0.1/stockdb?charset=utf8')
# #存入数据库
# df.to_sql('hist_data',engine)
dbA =dbOperate()
dbA.connectDb()
code ='600848'
df = ts.get_hist_data(code,ktype='M') 
print(df) 

for indexs in df.index:
    date = indexs
    opend =str(df.loc[indexs,["open"]].values[0])
    high=str(df.loc[indexs,["high"]].values[0])
    close =str(df.loc[indexs,["close"]].values[0])
    low =str(df.loc[indexs,["low"]].values[0])
    volume =str(df.loc[indexs,["volume"]].values[0])
    price_change =str(df.loc[indexs,["price_change"]].values[0])
    p_change =str(df.loc[indexs,["p_change"]].values[0])
    ma5 =str(df.loc[indexs,["ma5"]].values[0])
    ma10 =str(df.loc[indexs,["ma10"]].values[0])
    ma20 =str(df.loc[indexs,["ma20"]].values[0])
    v_ma5 =str(df.loc[indexs,["v_ma5"]].values[0])
    v_ma10 =str(df.loc[indexs,["v_ma10"]].values[0])
    v_ma20 =str(df.loc[indexs,["v_ma20"]].values[0])
    insert =("insert into  hist_data(code,date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20) values('"+code+"','"+date+"',"+opend+","+high+","+close+","+low+","+volume+","+price_change+","+p_change+","+ma5+","+ma10+","+ma20+","+v_ma5+","+v_ma10+","+v_ma20+")")
    print(insert)
    dbA.updateInsertDelete(insert)
dbA.commit()
# ts.get_hist_data('600848',ktype='W') #获取周k线数据
# ts.get_hist_data('600848',ktype='M') #获取月k线数据 
# ts.get_hist_data('600848',ktype='5') #获取5分钟k线数据 
# ts.get_hist_data('600848',ktype='15') #获取15分钟k线数据 
# ts.get_hist_data('600848',ktype='30') #获取30分钟k线数据 
# ts.get_hist_data('600848',ktype='60') #获取60分钟k线数据 
# ts.get_hist_data('sh')#获取上证指数k线数据，其它参数与个股一致，下同 
# ts.get_hist_data('sz')#获取深圳成指k线数据 ts.get_hist_data('hs300'）#获取沪深300指数k线数据 
# ts.get_hist_data('sz50')#获取上证50指数k线数据 
# ts.get_hist_data('zxb')#获取中小板指数k线数据 
# ts.get_hist_data('cyb')#获取创业板指数k线数据
