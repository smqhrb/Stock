import xlwt
import sys
import pandas as pd
import tushare as ts
import datetime
from datetime import timedelta
import getopt
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
    for o, a in opts:
        if o in ("-h", "--help"):
            print("---------help content------------------------------------------------------")
            print("|   -f fname          [get all stock data from config file]       ")
            print("|   -a                [all stock data save to one file 'stock.xls']       ")
            print("|   -s 2017-01-11     [start time,format YYYY-MM-DD]       ")
            print("|   -e 2018-01-11     [end   time,format YYYY-MM-DD]       ")
            print("|   for example:")
            print("|      example 1: all stock data write in one file 'stock.xls")
            print("|           python main.py -a a -f stockList.txt -s 2017-01-11 -e 2018-01-11")
            print("|      example 2: all stock data write in different files")
            print("|           python main.py -f stockList.txt -s 2017-01-11 -e 2018-01-11")
            print("|      example 3: default time is now to now -365day")
            print("|           python main.py -f stockList.txt")
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

    # files="stockList.txt"
    if len(files)>0:
        print("configure file name ="+files)
        if len(start)==0 and len(end)==0:
            now_time = datetime.datetime.now()
            end =now_time.strftime('%Y-%m-%d')
            lastyear_time =now_time -timedelta(days=365)
            start =lastyear_time.strftime('%Y-%m-%d')

        print("Start time ="+start)
        print("End time   ="+end)
        stockCodeList =readStockList(files)
        print("...start to read data...")
        if(len(allin)>0):
            getStockDataInOneFile(stockCodeList,'stock.xls',start,end)
        else:
            getStockDataInDifferentFile(stockCodeList,start,end)
        print("...end.................")
    else:
        print("...without stock code ,program end....")
        exit()
def getStockDataInDifferentFile(stockCodeList,start,end):

    for code in stockCodeList:
        print("...reading Stock ="+code+"...")
        df =ts.get_hist_data(code,start=start,end=end)
        savefileName =code+'.xls'
        writer = pd.ExcelWriter(savefileName)
        df.to_excel(writer,sheet_name=code)
        writer.save()
        print("...finish writing Stock ="+code+" data to "+savefileName)


def getStockDataInOneFile(stockCodeList,fname,start,end):
    writer = pd.ExcelWriter(fname)
    for code in stockCodeList:
        print("...reading Stock ="+code+"...")
        df =ts.get_hist_data(code,start=start,end=end)
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


if __name__ == '__main__':
    MainOpt()