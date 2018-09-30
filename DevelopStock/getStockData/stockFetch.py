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

    def profit_data(self,year,quarter):#盈利能力
        df =ts.get_profit_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            roe =str(df.loc[indexs,["roe"]].values[0])
            roe = '0' if roe in('nan','--') else roe
            net_profit_ratio =str(df.loc[indexs,["net_profit_ratio"]].values[0])
            net_profit_ratio = '0' if net_profit_ratio in('nan','--') else net_profit_ratio
            gross_profit_rate =str(df.loc[indexs,["gross_profit_rate"]].values[0])
            gross_profit_rate = '0' if gross_profit_rate in('nan','--') else gross_profit_rate
            net_profits =str(df.loc[indexs,["net_profits"]].values[0])
            net_profits = '0' if net_profits in('nan','--') else net_profits
            eps =str(df.loc[indexs,["eps"]].values[0])
            eps = '0' if eps in('nan','--') else eps
            business_income =str(df.loc[indexs,["business_income"]].values[0])
            business_income = '0' if business_income in('nan','--') else business_income
            bips =str(df.loc[indexs,["bips"]].values[0])
            bips = '0' if bips in('nan','--') else bips
            insert =("insert into  profit_data(code,name,roe,net_profit_ratio,gross_profit_rate,net_profits,eps,business_income,bips,year,quarter) values('"+code+"','"+name+"',"+roe+","+net_profit_ratio+","+gross_profit_rate+","+net_profits+","+eps+","+business_income+","+bips+",'"+str(year)+"','"+str(quarter)+"')")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()

    def operation_data(self,year,quarter):#营运能力
        df =ts.get_operation_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            arturnover =str(df.loc[indexs,["arturnover"]].values[0])
            arturnover = '0' if arturnover in('nan','--') else arturnover
            arturndays =str(df.loc[indexs,["arturndays"]].values[0])
            arturndays = '0' if arturndays in('nan','--') else arturndays
            inventory_turnover =str(df.loc[indexs,["inventory_turnover"]].values[0])
            inventory_turnover = '0' if inventory_turnover in('nan','--') else inventory_turnover
            inventory_days =str(df.loc[indexs,["inventory_days"]].values[0])
            inventory_days = '0' if inventory_days in('nan','--') else inventory_days
            currentasset_turnover =str(df.loc[indexs,["currentasset_turnover"]].values[0])
            currentasset_turnover = '0' if currentasset_turnover in('nan','--') else currentasset_turnover
            currentasset_days =str(df.loc[indexs,["currentasset_days"]].values[0])
            currentasset_days = '0' if currentasset_days in('nan','--') else currentasset_days
 
            insert =("insert into  operation_data(code,name,arturnover,arturndays,inventory_turnover,inventory_days,currentasset_turnover,currentasset_days,year,quarter) values('"+code+"','"+name+"',"+arturnover+","+arturndays+","+inventory_turnover+","+inventory_days+","+currentasset_turnover+","+currentasset_days+",'"+str(year)+"','"+str(quarter)+"')")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()


    def growth_data(self,year,quarter):#成长能力
        df =ts.get_growth_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            mbrg =str(df.loc[indexs,["mbrg"]].values[0])
            mbrg = '0' if mbrg=='nan' else mbrg
            nprg =str(df.loc[indexs,["nprg"]].values[0])
            nprg = '0' if nprg=='nan' else nprg
            nav =str(df.loc[indexs,["nav"]].values[0])
            nav = '0' if nav=='nan' else nav
            targ =str(df.loc[indexs,["targ"]].values[0])
            targ = '0' if targ=='nan' else targ
            epsg =str(df.loc[indexs,["epsg"]].values[0])
            epsg = '0' if epsg=='nan' else epsg
            seg =str(df.loc[indexs,["seg"]].values[0])
            seg = '0' if seg=='nan' else seg
            insert =("insert into  growth_data(code,name,mbrg,nprg,nav,targ,epsg,seg,year,quarter) values('"+code+"','"+name+"',"+mbrg+","+nprg+","+nav+","+targ+","+epsg+","+seg+",'"+str(year)+"','"+str(quarter)+"')")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()

    def debtpaying_data(self,year,quarter):#偿债能力
        df =ts.get_debtpaying_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            currentratio =str(df.loc[indexs,["currentratio"]].values[0])
            currentratio = '0' if currentratio in('nan','--') else currentratio
            quickratio =str(df.loc[indexs,["quickratio"]].values[0])
            quickratio = '0' if quickratio in('nan','--') else quickratio
            cashratio =str(df.loc[indexs,["cashratio"]].values[0])
            cashratio = '0' if cashratio in('nan','--') else cashratio
            icratio =str(df.loc[indexs,["icratio"]].values[0])
            icratio = '0' if icratio in('nan','--') else icratio
            sheqratio =str(df.loc[indexs,["sheqratio"]].values[0])
            sheqratio = '0' if sheqratio in('nan','--') else sheqratio
            adratio =str(df.loc[indexs,["adratio"]].values[0])
            adratio = '0' if adratio in('nan','--') else adratio
 
            insert =("insert into  debtpaying_data(code,name,currentratio,quickratio,cashratio,icratio,sheqratio,adratio,year,quarter)\
                                values('"+code+"','"+name+"',"+currentratio+","+quickratio+","+cashratio+","+icratio+","+sheqratio+","+adratio+",'"+str(year)+"','"+str(quarter)+"')")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()

    def cashflow_data(self,year,quarter):#现金流量
        df =ts.get_cashflow_data(year,quarter)   
        for indexs in df.index:
            code =str(df.loc[indexs,["code"]].values[0])
            name =str(df.loc[indexs,["name"]].values[0])
            cf_sales  =str(df.loc[indexs,["cf_sales"]].values[0])
            cf_sales ='0' if cf_sales in('nan','--') else cf_sales
            rateofreturn =str(df.loc[indexs,["rateofreturn"]].values[0])
            rateofreturn = '0' if rateofreturn in('nan','--') else rateofreturn
            cf_nm =str(df.loc[indexs,["cf_nm"]].values[0])
            cf_nm = '0' if cf_nm in('nan','--') else cf_nm
            cf_liabilities =str(df.loc[indexs,["cf_liabilities"]].values[0])
            cf_liabilities = '0' if cf_liabilities in('nan','--') else cf_liabilities
            cashflowratio =str(df.loc[indexs,["cashflowratio"]].values[0])
            cashflowratio = '0' if cashflowratio in('nan','--') else cashflowratio
 
            insert =("insert into  cashflow_data(code,name,cf_sales,rateofreturn,cf_nm,cf_liabilities,cashflowratio,year,quarter) values('"+code+"','"+name+"',"+cf_sales+","+rateofreturn+","+cf_nm+","+cf_liabilities+","+cashflowratio+",'"+str(year)+"','"+str(quarter)+"')")            
            self.dbA.updateInsertDelete(insert)
        self.dbA.commit()


if __name__ == '__main__':
    tg =tushareGet()
    year =2017
    quarter =1
    # tg.stock_basics()
    # tg.hist_data()
    # tg.profit_data(2017,1) #fail to get data
    # 
    # tg.growth_data(year,quarter)
    # tg.operation_data(year,quarter)
    # tg.debtpaying_data(year,quarter)
    # tg.cashflow_data(year,quarter)

    

