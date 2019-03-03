import xlwt
import sys
import os
import pandas as pd
import tushare as ts
import datetime
from datetime import timedelta
from drawStockCurve import stockCurve
import getopt
print("Script name：",sys.argv[0])
print("")
len1 =len(sys.argv)

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'a:f:s:e:d:h',['all=','files=','start=','end=','draw=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()

    files=""
    allin =""
    start =""
    end =""
    drawPic =""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("---------help content------------------------------------------------------")
            print("|   -f fname          [get all stock data from config file]       ")
            print("|   -a                [all stock data save to one file 'stock.xls']       ")
            print("|   -s 20170111       [start time,format YYYYMMDD]                       ")
            print("|   -e 20180111       [end   time,format YYYYMMDD]                 ")
            print("|   -d 000882.SZ.xls  [file name for draw KLine Colume MACD]       ")
            
            print("|   for example:")
            print("|      example 1: all stock data write in one file 'stock.xls")
            print("|           python main.py -a a -f stockList.txt -s 20170111 -e 20180111")
            print("|      example 2: all stock data write in different files")
            print("|           python main.py -f stockList.txt -s 20170111 -e 20180111")
            print("|      example 3: default time is now to now -365day")
            print("|           python main.py -f stockList.txt")
            print("|      example 4: draw Kline Colume MACD")
            print("|           python main.py -d 000882.SZ.xls")
            print("|                                           ")
            print("|   stock code is 601800.SH or 300298.SZ or 000882.SZ")
            print("---------------------------------------------------------------------------------")
            sys.exit()
        elif o in ("-f", "--files"):
            files = a
        elif o in ("-a","--all"):
            allin ="a"
        elif o in ("-s","--start"):
            start =a
        elif o in ("-e","--end"):
            end =a
        elif o in ("-d","--draw"):
            drawPic =a
        else:
            sys.exit()

    print("Please confirm xls file not to be covered in current folder")
    print("Continue? Please input 'y' to continune,'n' to end this program.")
    str = input("Enter your input: ")
    if str=='n':
        exit()
    elif str=='y':
        pass
    if(len(drawPic)>0):
        if os.path.exists(drawPic):
            getXlsDataForDraw(drawPic)
        exit()
    # files="stockList.txt"
    if len(files)>0:
        print("configure file name ="+files)
        if len(start)==0 and len(end)==0:
            now_time = datetime.datetime.now()
            # end =now_time.strftime('%Y-%m-%d')
            # lastyear_time =now_time -timedelta(days=365)
            # start =lastyear_time.strftime('%Y-%m-%d')
            end =now_time.strftime('%Y%m%d')
            lastyear_time =now_time -timedelta(days=365)
            start =lastyear_time.strftime('%Y%m%d')

        print("Start time ="+start)
        print("End time   ="+end)
        stockCodeList =readStockList(files)
        print("...start to read data...")
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
        
        if(len(allin)>0):
            getStockDataInOneFile(stockCodeList,'stock.xls',start,end)
        else:
            getStockDataInDifferentFile(stockCodeList,start,end)
        print("...end.................")
    else:
        print("...without stock code ,program end....")
        exit()
def getStockDataInDifferentFile(stockCodeList,start,end):
    pro = ts.pro_api()
    for code in stockCodeList:
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

        df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
        df=df1.sort_values(by=['trade_date'])
        # df.drop(['index'],axis=1,inplace=True)
        df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
        savefileName =code+'.xls'
        writer = pd.ExcelWriter(savefileName)
        df.to_excel(writer,sheet_name=code)

        writer.save()
        print("...finish writing Stock ="+code+" data to "+savefileName)


def getStockDataInOneFile(stockCodeList,fname,start,end):
    writer = pd.ExcelWriter(fname)
    pro = ts.pro_api()
    for code in stockCodeList:
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'}, inplace = True)
        df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
        df=df1.sort_values(by=['trade_date'])
        # df.drop(['index'],axis=1,inplace=True)
        df.to_excel(writer,sheet_name=code)   
    writer.save()
    print("...finish writing Stock data to "+fname)

def readStockList(fname):
    contents =[]
    f = open(fname)
    lines = f.readlines()
    for code in lines:
        k =code.strip()
        if len(k)>0:
            contents.append(k)
    f.close()
    print("....Stock Code List............")
    print(contents)
    return contents
def getXlsDataForDraw(fileName):
    xlsData =pd.read_excel(fileName)
    df_raw =pd.DataFrame()
    df_raw['t'] =xlsData['交易日期']
    df_raw['open']=xlsData['开盘价']
    df_raw['high']=xlsData['最高价']
    df_raw['low']=xlsData['最低价']
    df_raw['close']=xlsData['收盘价']
    df_raw['volume']=xlsData['成交量 （手）']  
    drawPic =stockCurve(df_raw)
    drawPic.drawAll() 

if __name__ == '__main__':
    MainOpt()