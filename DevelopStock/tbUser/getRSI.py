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
            print("---------帮助信息------------------------------------------------------")
            print("|   -f fname    [从文件fname获取股票代码.当fname是all_stock时是获取市场上所有股票代码]")
            print("|   -s 20170111 [起始日期,format YYYYMMDD]")
            print("|   -e 20180111 [结束,format YYYYMMDD.如果是Now,就是到今天]")
                        
            print("|  例子:")
            print("|      例1: 一个股票写入一个xls文件")
            print("|           python getRSI.py -f stockList.txt -s 20170111 -e 20180111")
            print("|           python getRSI.py -f all_stock -s 20170111 -e 20180111")
            print("|           python getRSI.py -f stockList.txt -s 20150101 -e Now")
            print("|           python getRSI.py -f all_stock -s 20150101 -e Now")
            print("|      例2: 缺省时间是  一年前的今天 到 今天")
            print("|           python getRSI.py -f stockList.txt")
            print("|                                           ")
            print("|   股票代码格式 是 601800.SH 或者 300298.SZ 或者 000882.SZ")
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

    print("在当前目录下请确认没有xls文件被覆盖.续输入y,结束输入n?")
    str = input("请输入: ")
    if str=='n':
        exit()
    elif str=='y':
        pass

    if len(files)>0:
        print("configure file name ="+files)
        if len(start)==0 and len(end)==0:
            now_time = datetime.datetime.now()
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
    inputConfirm =""
    for code in (stockCodeList):
        savefileName =path+'/'+code+'.xls'
        i =i+1
        
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            if(len(inputConfirm)<=0):
                inputConfirm = input("更新最新的数据到已经存在的文件中吗？更新输入y,不更新输入n: ")
            if inputConfirm=='n':
                continue
            elif inputConfirm=='y':
                pass
            df0 =pd.read_excel(savefileName)
            df0 =df0.drop(['indexU','RSI6','RSI12','RSI24'],axis=1)
            start =str(df0.trade_date.max()+1)
            print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
            time.sleep(0.3)
            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df0 =df0.append(df1)
            df0 =df0.set_index(['trade_date'])
            df0.index =df0.index.astype(int)
            df0=df0.sort_index()
            df =df0.reset_index()
            
            df['RSI6'] =RSI(df.close,6)
            df['RSI12'] =RSI(df.close,12)
            df['RSI24'] =RSI(df.close,24)        
        else:    
            print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
             # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)
            time.sleep(0.3)
            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df=df1.sort_values(by=['trade_date'])
            lenTh =len(df)
            df['indexU'] =np.arange(0,lenTh,1)
            df =df.set_index(['indexU'])
            df['RSI6'] =RSI(df.close,6)
            df['RSI12'] =RSI(df.close,12)
            df['RSI24'] =RSI(df.close,24)      
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
