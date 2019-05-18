import xlwt
import sys
import os
import time
import pandas as pd
import tushare as ts
import datetime
from datetime import timedelta
from drawStockCurve import stockCurve
import getopt
import numpy as np
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
    path ="./%sTo%s"%(start,end)
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    pro = ts.pro_api()
    i=0
    for code in stockCodeList:
        savefileName =path+'/'+code+'('+start+'To'+end+').xls'
        i =i+1
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            continue
        time.sleep(0.3)
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

        df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
        df1['RSI6'] =RSI(df1.Close,6)
        df1['RSI12'] =RSI(df1.Close,12)
        df1['RSI24'] =RSI(df1.Close,24)      
        df=df1.sort_values(by=['trade_date'])
  
        # df.drop(['index'],axis=1,inplace=True)

        #df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)

        writer = pd.ExcelWriter(savefileName)
        df.to_excel(writer,sheet_name=code)

        writer.save()
        print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))

def getStockDataInDifferentFileUser(stockCodeList,start,end):
    path ="./%sTo%s"%(start,end)
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    pro = ts.pro_api()
    i=0
    for code in stockCodeList:
        savefileName =path+'/'+code+'('+start+'To'+end+').xlsx'
        i =i+1
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            print("...reading fileName =%s"%savefileName)
            df1 = pd.read_excel(savefileName)
            df1.rename(columns={'股票代码':'ts_code','交易日期':'trade_date','开盘价':'open','最高价':'high','最低价':'low','收盘价':'close','昨收价':'pre_close','涨跌额':'change','涨跌幅(未复权)':'pct_chg','成交量 （手）':'vol','成交额(千元)':'amount'}, inplace = True)
            # df=df1.sort_values(by=['trade_date'])
            df =df1
        else:
            time.sleep(0.3)
            print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
            # df =ts.get_hist_data(code,start=start,end=end)
            # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

            df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
            df=df1.sort_values(by=['trade_date'])
            df=df.reset_index()
            df.drop(['index'],axis=1,inplace=True)
        ####
        #比如002321这份数据 第71行（2018年6月1日）
        # 最高价等于昨收价的1.1倍（四舍五入）
        # 并且6月1日的最高价未高于其前5个交易的最高价（即前5个交易日有价格高于6月1日的最高价即可）  
        # 数据符合条件 然后在该行后标记个1，在其后面一行（72行）标记为2   
        # 做标记的目的是方便筛选
        

        df_temp =df[round(df['high']/df['pre_close'],2)==1.1]
        df['flag']=''
        for j in range(len(df_temp)):
            ind =df_temp.index[j]
            if(ind>5):
                value =df.iloc[ind]['high']
                if((df.iloc[ind-1]['high']>=value) or (df.iloc[ind-2]['high']>=value) or (df.iloc[ind-3]['high']>=value) or (df.iloc[ind-4]['high']>=value)  or (df.iloc[ind-5]['high']>=value)):
                    df.loc[ind,'flag'] =1
                    df.loc[ind+1,'flag']=2        
        ####
        df['最高涨幅'] =df['high']/df['pre_close'] -1
        df['最低涨幅'] =df['low']/df['pre_close'] -1
        df['收盘涨幅'] =df['close']/df['pre_close'] -1
        df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
        order =['股票代码','交易日期','开盘价','最高价','最高涨幅','最低价','最低涨幅','收盘价','收盘涨幅','昨收价','涨跌额','涨跌幅(未复权)','成交量 （手）','成交额(千元)','flag']
        dfR =df[order]
        writer = pd.ExcelWriter(savefileName)
        dfR.to_excel(writer,sheet_name=code)

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
def getIndexDay(indexCode,fname,start,end):
    '''
    获取指数数据
    000001.Sh -上证指数 
    399001.Sz -深证成指
    不成功因为积分不够
    '''
    ts.set_token('582c8c9ab1bd9e3e14d5d60527d63affb8c310fba3fb9f5d7853bf9c')
    pro = ts.pro_api()
    df1 = pro.index_daily(ts_code=indexCode, start_date=start, end_date=end)
    df=df1.sort_values(by=['trade_date'])
    writer = pd.ExcelWriter(fname)
    df.to_excel(writer,sheet_name=indexCode) 

    
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
def dataProcess(fname,code):
    df1 = pd.read_excel(fname)
    df=df1.sort_values(by=['交易日期'])
    df['收益率%'] =round(100*(df['收盘价'] -df['收盘价'].shift(-1))/df['收盘价'].shift(-1),2)
    writer = pd.ExcelWriter('good'+fname)
    df.to_excel(writer,sheet_name=code) 
    writer.save()

def calcMacd(data,fast_period=12,slow_period=26,signal_period=9): 
    # data['close'] -- 收盘价 
    # 收盘价按照日期升序( data['date'] )排列 
    # 返回值都是 Series 
    fast_ewm=data['close'].ewm(span=fast_period).mean() 
    slow_ewm=data['close'].ewm(span=slow_period).mean() 
    dif=fast_ewm-slow_ewm 
    dea=dif.ewm(span=signal_period).mean() 
    # 一般概念里，macd柱是 (dif-dea)*2，实际上只是为了扩大显示效果 
    # # 实测后发现，也可以不乘以2，效果也足够清楚了 
    macd=(dif-dea)*2 
    # 将bar 分成红绿柱分别导出数据， 
    return dif,dea,macd

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

def getMacdCrossPoint(diff,dea):
    '''
    get the cross point,
    parameter:
        diff is diff
        dea is dea
    return : retU is diff up corss dea
                retD is diff down cross dea
    '''
    crossPoint =diff - dea
    iCount = len(crossPoint)
    retU =[]
    retD =[]
    i=1
    while i<iCount:
        flag =crossPoint[i]*crossPoint[i-1]
        if flag<0:
            if crossPoint[i]>0:
                retU.append(i)
            else:
                retD.append(i)
        i=i+1
    return np.array(retU),np.array(retD)

def walkDirData(path):
    '''
    遍历文件夹下的原始数据
    '''
    file_list = os.listdir(path)
    for f in file_list:
        dataRead(path,f)
 
    
def dataRead(path,fn):
    '''
    计算macd金叉和死叉之间的收益
    '''
    df1 = pd.read_excel(path+'/'+fn)
    
    dif,dea,macd =calcMacd(df1)
    df1['dif'] =dif
    df1['dea'] =dea
    df1['macd'] =macd
    df1['sub'] = dif - dea
    # dif =df1['dif']
    # dea =df1['dea']

    maxLen =len(dif)
    u,d =getMacdCrossPoint(dif,dea)
    # print(u)
    # print(d)
    dfu =df1.iloc[maxLen-u-1,:]
    dfd =df1.iloc[maxLen-d-1,:] 
    # dfu =df1.iloc[u,:]
    # dfd =df1.iloc[d,:] 

    dfh =dfu.append(dfd)
    df=dfh.sort_values(by=['trade_date'])
    df['macd 收益'] = df['close'] -df['close'].shift(1)
    writer = pd.ExcelWriter(path+'/ok'+fn)
    
    df1.to_excel(writer,sheet_name=fn[0:6]) 
    df.to_excel(writer,sheet_name='hb') 
    writer.save()    
def getUp10(start,end):
    '''
    弄一份10年到现在连续涨停超过3天的数据，去除St里面需要有这几天的日期和股票号码
    我需要开始涨停的日期和结束的，这两个比较重要
    不需要是完全连续一字涨停，只要连续三天收盘价是涨停就可以
    新上市也帮我排除
    '''
    path ="./%sTo%s"%(start,end)
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    pro = ts.pro_api()
    i=0
    codeList = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,list_date')#TS代码,代码,名称,上市日期
    #stockCodeList =codeList['ts_code'].tolist()
    dfResult =pd.DataFrame()
    writerR = pd.ExcelWriter('resultTop10.xls')
    # for code in stockCodeList:
    for i in range(0, len(codeList)):
        #code ='000651.SZ'
        code =codeList.iloc[i]['ts_code']
        list_date =codeList.iloc[i]['list_date']
        name =codeList.iloc[i]['name']
        if(name.find('ST')>=0):
            print('skip name=%s,code=%s'%(name,code))
            continue
        savefileName =path+'/'+code+'('+start+'To'+end+').xls'
        # i =i+1
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            continue
        time.sleep(0.3)
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

        df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
        df=df1.sort_values(by=['trade_date'])
        df=df.reset_index()
        df.drop(['index'],axis=1,inplace=True)
        dfTop10 =df[df['pct_chg']>9.98]
        for j in range(len(dfTop10)):
            if(j>=3):
                if((dfTop10.index[j] -dfTop10.index[j-1])==1):
                    if((dfTop10.index[j-1] -dfTop10.index[j-2])==1):
                        
                            dfTmp =dfTop10.iloc[j-2]
                            dfTmp['name'] =name
                            dfTmp['list_date'] =list_date
                            dfResult =dfResult.append(dfTmp)
                            dfTmp =dfTop10.iloc[j-1]
                            dfTmp['name'] =name
                            dfTmp['list_date'] =list_date                            
                            dfResult =dfResult.append(dfTmp)
                            dfTmp =dfTop10.iloc[j]
                            dfTmp['name'] =name
                            dfTmp['list_date'] =list_date
                            dfResult =dfResult.append(dfTmp)
        #df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
        writer = pd.ExcelWriter(savefileName)
        dfTop10.to_excel(writer,sheet_name=code)
        writer.save()
        print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))

    dfResult =dfResult.drop_duplicates()
    order =['ts_code','name','trade_date','open','high','low','close','pre_close','change','pct_chg','vol','amount','list_date']
    dfR =dfResult[order]
    dfR.to_excel(writerR,sheet_name='Result')
    writerR.save()

def flagTop10(stockCodeList,start,end):
    '''
    最高价等于昨收价的1.1倍（四舍五入）
    并且6月1日的最高价未高于其前5个交易的最高价（即前5个交易日有价格高于6月1日的最高价即可）  
    数据符合条件 然后在该行后标记个1，在其后面一行（72行）标记为2   
    做标记的目的是方便筛选
    '''
    path ="./%sTo%s"%(start,end)
    if(os.path.exists(path)==False): #判断目标是否存在 
        os.mkdir(path) #创建目录
    pro = ts.pro_api()
    i=0
    for code in stockCodeList:
        savefileName =path+'/'+code+'('+start+'To'+end+').xls'
        i =i+1
        if(os.path.exists(savefileName)):
            print("...[%d]%s exist"%(i,savefileName))
            continue
        time.sleep(0.3)
        print("...reading Stock ="+code+" from "+ start +" to "+end+" ...")
        # df =ts.get_hist_data(code,start=start,end=end)
        # df.rename(columns={'date':'日期', 'open':'开盘价','high':'最高价','close':'收盘价','low':'最低价','volume':'成交量','price_change':'价格变动','p_change':'涨跌幅','ma5':'5日均价','ma10':'10日均价','ma20':'20日均价','v_ma5':'5日均量','v_ma10':'10日均量','v_ma20':'20日均量','turnover':'换手率'},inplace = True)

        df1 = pro.daily(ts_code=code, start_date=start, end_date=end)
        df=df1.sort_values(by=['trade_date'])
        ####
        #比如002321这份数据 第71行（2018年6月1日）
        # 最高价等于昨收价的1.1倍（四舍五入）
        # 并且6月1日的最高价未高于其前5个交易的最高价（即前5个交易日有价格高于6月1日的最高价即可）  
        # 数据符合条件 然后在该行后标记个1，在其后面一行（72行）标记为2   
        # 做标记的目的是方便筛选
        df=df.reset_index()
        df.drop(['index'],axis=1,inplace=True)
        # df.drop(['index'],axis=1,inplace=True)
        df_temp =df[round(df['high']/df['pre_close'],2)==1.1]
        df['flag']=''
        for j in range(len(df_temp)):
            ind =df_temp.index[j]
            if(ind>5):
                value =df.iloc[ind]['high']
                if((df.iloc[ind-1]['high']>=value) or (df.iloc[ind-2]['high']>=value) or (df.iloc[ind-3]['high']>=value) or (df.iloc[ind-4]['high']>=value)  or (df.iloc[ind-5]['high']>=value)):
                    df.loc[ind,'flag'] =1
                    df.loc[ind+1,'flag']=2        
        ####
        df['最高涨幅'] =df['high']/df['pre_close'] -1
        df['最低涨幅'] =df['low']/df['pre_close'] -1
        df['收盘涨幅'] =df['close']/df['pre_close'] -1
        df.rename(columns={'ts_code':'股票代码','trade_date':'交易日期','open':'开盘价','high':'最高价','low':'最低价','close':'收盘价','pre_close':'昨收价','change':'涨跌额','pct_chg':'涨跌幅(未复权)','vol':'成交量 （手）','amount':'成交额(千元)'}, inplace = True)
        order =['股票代码','交易日期','开盘价','最高价','最高涨幅','最低价','最低涨幅','收盘价','收盘涨幅','昨收价','涨跌额','涨跌幅(未复权)','成交量 （手）','成交额(千元)','flag']
        dfR =df[order]
        writer = pd.ExcelWriter(savefileName)
        dfR.to_excel(writer,sheet_name=code)

        writer.save()
        print("...[%d]finish writing Stock =%s data to %s"%(i,code,savefileName))
    

if __name__ == '__main__':
    #tb775860
    now_time = datetime.datetime.now()
    end =now_time.strftime('%Y%m%d')
    getUp10('20100101',end)
    #tb775860 end
    # MainOpt()
    # getIndexDay('000001.SH','000001Index.xls','20180201','20180411')	
	# dataProcess('000001.xls','000001')
	# dataProcess('399001.xls','399001')
    # walkDirData('./20170601To20190131')
    #dataRead('.','002230_1.xls')
    # dataRead('.','002460_1.xls')
    # dataRead('.','603799_1.xls')
    #calcRSI('.','002460_1.xls')
    #dataProcess('002024SZ.xls','002024SZ')
    #