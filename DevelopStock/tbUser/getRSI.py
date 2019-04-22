import xlwt
import sys
import os
import time
import pandas as pd
import tushare as ts
import datetime
from datetime import timedelta
import getopt
import numpy as np
print("Script name：",sys.argv[0])
print("")
len1 =len(sys.argv)

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'a:f:s:e:h',['all=','files=','start=','end=','help'])
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
                        
            print("|   for example:")
            print("|      example 1: all stock data write in one file 'stock.xls")
            print("|           python main.py -a a -f stockList.txt -s 20170111 -e 20180111")
            print("|      example 2: all stock data write in different files")
            print("|           python main.py -f stockList.txt -s 20170111 -e 20180111")
            print("|           python main.py -f stockList.txt -s 20170111 -e Now")
            print("|      example 3: default time is now to now -365day")
            print("|           python main.py -f stockList.txt")
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
        else:
            sys.exit()

    print("Please confirm xls file not to be covered in current folder")
    print("Continue? Please input 'y' to continune,'n' to end this program.")
    str = input("Enter your input: ")
    if str=='n':
        exit()
    elif str=='y':
        pass
    files="stockList.txt"
    start ="20150101"
    end ="Now"
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
        if(files =="all_stock"):
            stockCodeList=""
            pass
        else:
            stockCodeList =readStockList(files)
        print("...start to read data...")
        ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
        
        if(len(allin)>0):
            getStockDataInOneFile(stockCodeList,'stock.xls',start,end)
        else:
            if(end =='Now'):
                now_time = datetime.datetime.now()
                end =now_time.strftime('%Y%m%d')
            getStockDataInDifferentFile(stockCodeList,start,end)
        print("...end.................")
    else:
        print("...without stock code ,program end....")
        exit()
def getStockDataInDifferentFile(stockCodeList,start,end):
    path ="./%s"%('Result')
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    pro = ts.pro_api()
    i=0
    if(stockCodeList ==""):
        data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
        stockCodeList =data.ts_code
    for code in (stockCodeList):
    # for code in stockCodeList:
        savefileName =path+'/'+code+'.xls'
        i =i+1
        time.sleep(0.3)
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            df0 =pd.read_excel(savefileName)
            df0 =df0.drop(['indexU','RSI6','RSI12','RSI24'],axis=1)
            start =str(df0.trade_date.max()+1)
            print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df0 =df0.append(df1)
            df0.reset_index()
            df=df0.sort_values(by=['trade_date'])
            
            df['RSI6'] =RSI(df.close,6)
            df['RSI12'] =RSI(df.close,12)
            df['RSI24'] =RSI(df.close,24)        
            
            
        else:    
            
            print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
            # df =ts.get_hist_data(code,start=start,end=end)
            # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df=df1.sort_values(by=['trade_date'])
            lenTh =len(df)
            df['indexU'] =np.arange(0,lenTh,1)
            df =df.set_index(['indexU'])
            df['RSI6'] =RSI(df.close,6)
            df['RSI12'] =RSI(df.close,12)
            df['RSI24'] =RSI(df.close,24)      

    
            # df.drop(['index'],axis=1,inplace=True)

            #df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)

        writer = pd.ExcelWriter(savefileName)
        df.to_excel(writer,sheet_name=code)

        writer.save()
        print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))


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

def RSI(t, periods=6):
    '''
    计算RSI 正确
    '''
    length = len(t)
    rsies = [np.nan]*length
    #数据长度不超过周期，无法计算；
    if length <= periods:
        return rsies
    #用于快速计算；
    up_avg = 0
    down_avg = 0

    #首先计算第一个RSI，用前periods+1个数据，构成periods个价差序列;
    first_t = t[:periods+1]
    for i in range(1, len(first_t)):
        #价格上涨;
        if first_t[i] >= first_t[i-1]:
            up_avg += first_t[i] - first_t[i-1]
        #价格下跌;
        else:
            down_avg += first_t[i-1] - first_t[i]
    up_avg = up_avg / periods
    down_avg = down_avg / periods
    rs = up_avg / down_avg
    rsies[periods] = 100 - 100/(1+rs)

    #后面的将使用快速计算；
    for j in range(periods+1, length):
        up = 0
        down = 0
        if t[j] >= t[j-1]:
            up = t[j] - t[j-1]
            down = 0
        else:
            up = 0
            down = t[j-1] - t[j]
        #类似移动平均的计算公式;
        up_avg = (up_avg*(periods - 1) + up)/periods
        down_avg = (down_avg*(periods - 1) + down)/periods
        rs = up_avg/down_avg
        rsies[j] = 100 - 100/(1+rs)
    return rsies  
def calcRSI(path,fn):
    df1 = pd.read_excel(path+'/'+fn)
    df1['RSI6'] =RSI(df1.Close,6)
    df1['RSI12'] =RSI(df1.Close,12)
    df1['RSI24'] =RSI(df1.Close,24)
    writer = pd.ExcelWriter(path+'/RSI'+fn)
    
    df1.to_excel(writer,sheet_name=fn[0:6]) 
    writer.save()   

    


if __name__ == '__main__':
    MainOpt()
    # getIndexDay('000001.SH','000001Index.xls','20180201','20180411')	
	# dataProcess('000001.xls','000001')
	# dataProcess('399001.xls','399001')
    # walkDirData('./20170601To20190131')
    #dataRead('.','002230_1.xls')
    # dataRead('.','002460_1.xls')
    # dataRead('.','603799_1.xls')
    # calcRSI('.','002460_1.xls')
    #dataProcess('002024SZ.xls','002024SZ')
    #