'''Hu Shen 300'''
HS300 ='hs300.xls'
'''Shen Zhen 50 '''
ZZ50 ='zz50.xls'
'''Zhong Zhen 500 '''
ZZ500='zz500.xls'
STOCKLIST ='stockList.xls'
SINA_NEWS ='sinaNews_from%s to%s'
import tushare as ts
import pandas as pd
class stockBase:
    def __init__(self):
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
        self.pro = ts.pro_api()
        
    def getHs300(self):
        print("...reading HS300 ...")
        df1 =ts.get_hs300s()
        writer = pd.ExcelWriter(HS300)
        df=df1.sort_values(by=['code'])
        df.to_excel(writer,sheet_name='hs300')   
        writer.save()
        print("...saved HS300 ...")
    def getZZ50(self):
        print("...reading ZZ50 ...")
        df1 =ts.get_sz50s()
        writer = pd.ExcelWriter(ZZ50)
        df=df1.sort_values(by=['code'])
        df.to_excel(writer,sheet_name='ZZ50')   
        writer.save()
        print("...saved ZZ50 ...")       
    def getZZ500(self):
        print("...reading ZZ500 ...")
        df1 =ts.get_zz500s()
        writer = pd.ExcelWriter(ZZ500)
        df=df1.sort_values(by=['code'])
        df.to_excel(writer,sheet_name='ZZ500')   
        writer.save()
        print("...saved ZZ500 ...")
    def getStockList(self):
        print("...reading Stock List ...")
        df1 = self.pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        writer = pd.ExcelWriter(STOCKLIST)
        df=df1.sort_values(by=['ts_code'])
        df.to_excel(writer,sheet_name='STOCKLIST')   
        writer.save()
        print("...saved Stock List ...")

    def getSinaNewsOfStock(self,startDate,endDate):
        df = self.pro.news(src='sina', start_date=startDate, end_date=endDate)
        writer = pd.ExcelWriter(SINA_NEWS%(startDate,endDate))
        df.to_excel(writer,sheet_name='Sina News')  
        writer.save() 
        # print(SINA_NEWS%(startDate,endDate))


if __name__ == '__main__':
    base =stockBase()
    # base.getHs300()
    # base.getZZ50()
    # base.getZZ500()
    # base.getStockList()
    base.getSinaNewsOfStock('20181101','20190201')



