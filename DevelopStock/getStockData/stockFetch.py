import urllib3
import tushare as ts
import pandas as pd
import sys
sys.path.append('E:\\Project\\Stock\DevelopStock\\')
# sys.path.append('../UI')
# import UI
from Config import dbOperate
################
# import pymysql
# pymysql.install_as_MySQLdb()
# sys.path.append(r'..\UI')
# from sqlalchemy import create_engine
# import tushare as ts
# df = ts.get_hist_data('600848')
# engine = create_engine('mysql://root:smq1234@127.0.0.1/stockdb?charset=utf8')
# #存入数据库
# df.to_sql('hist_data',engine)
######################

# dbA =dbOperate()
# dbA.connectDb()
# code ='600848'
# df = ts.get_hist_data(code,ktype='M') 
# print(df) 

# for indexs in df.index:
#     date = indexs
#     opend =str(df.loc[indexs,["open"]].values[0])
#     high=str(df.loc[indexs,["high"]].values[0])
#     close =str(df.loc[indexs,["close"]].values[0])
#     low =str(df.loc[indexs,["low"]].values[0])
#     volume =str(df.loc[indexs,["volume"]].values[0])
#     price_change =str(df.loc[indexs,["price_change"]].values[0])
#     p_change =str(df.loc[indexs,["p_change"]].values[0])
#     ma5 =str(df.loc[indexs,["ma5"]].values[0])
#     ma10 =str(df.loc[indexs,["ma10"]].values[0])
#     ma20 =str(df.loc[indexs,["ma20"]].values[0])
#     v_ma5 =str(df.loc[indexs,["v_ma5"]].values[0])
#     v_ma10 =str(df.loc[indexs,["v_ma10"]].values[0])
#     v_ma20 =str(df.loc[indexs,["v_ma20"]].values[0])
#     insert =("insert into  hist_data(code,date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20) values('"+code+"','"+date+"',"+opend+","+high+","+close+","+low+","+volume+","+price_change+","+p_change+","+ma5+","+ma10+","+ma20+","+v_ma5+","+v_ma10+","+v_ma20+")")
#     print(insert)
#     dbA.updateInsertDelete(insert)
# dbA.commit()
##############
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

class tushareGet:
    def __init__(self):
        self.code ="all"
        self.dbA =dbOperate()
        self.dbA.connectDb()

    def stock_basics(self):
        df =ts.get_stock_basics()
        for indexs in df.index:
            stockCode =indexs
            name =str(df.loc[indexs,["name"]].values[0])
            industry =str(df.loc[indexs,["industry"]].values[0])
            area =str(df.loc[indexs,["area"]].values[0])
            pe =str(df.loc[indexs,["pe"]].values[0])
            outstanding =str(df.loc[indexs,["outstanding"]].values[0])
            totals =str(df.loc[indexs,["totals"]].values[0])
            totalAssets =str(df.loc[indexs,["totalAssets"]].values[0])
            insert = ("insert into stock_basics(code,name,industry,area,pe,outstanding,totals,totalAssets) values('"+\
                         stockCode+"','"+name+"','"+industry+"','"+area+"',"+pe+","+outstanding+","+totals+","+totalAssets+")")
            print(stockCode)
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()
    
    def hist_data(self,code,ktype):
        df = ts.get_hist_data(code,ktype=ktype) 
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
            # print(insert)
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()

    def profit_data(self,year,quarter):
        df =ts.get_profit_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            roe =str(df.loc[indexs,["roe"]].values[0])
            net_profit_ratio =str(df.loc[indexs,["net_profit_ratio"]].values[0])
            gross_profit_rate =str(df.loc[indexs,["gross_profit_rate"]].values[0])
            net_profits =str(df.loc[indexs,["net_profits"]].values[0])
            eps =str(df.loc[indexs,["eps"]].values[0])
            business_income =str(df.loc[indexs,["business_income"]].values[0])
            bips =str(df.loc[indexs,["bips"]].values[0])
            insert =("insert into  profit_data(code,name,roe,net_profit_ratio,gross_profit_rate,net_profits,eps,business_income,bips) values('"+code+"','"+name+"',"+roe+","+net_profit_ratio+","+gross_profit_rate+","+net_profits+","+eps+","+business_income+","+bips+")")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()

if __name__ == '__main__':
    tg =tushareGet()
    #tg.stock_basics()
    #tg.hist_data()
    tg.profit_data(2017,1) #fail to get data

