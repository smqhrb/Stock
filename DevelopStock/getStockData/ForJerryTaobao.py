#coding=utf-8
import getopt
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import urllib.request as urllib2
from bs4 import BeautifulSoup 
import random
from html.parser import HTMLParser
import time
class RandomHeader:
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0(Macintosh;IntelMacOSX10.6;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1)",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)"
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def GetHeader(self):
        headers={"User-Agent":random.choice(self.user_agent_list)}
        return headers
class AccountPd:
    '''
    获取分红 和 最新 股票列表
    '''
    def __init__(self,destPath=".\\Account\\"):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""

        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            print("current path=%s"%(os.getcwd()))
            print("%s exist"%(self.destPath))
            pass
        else:
            os.mkdir(destPath)
            print("current path=%s"%(os.getcwd()))
            print("create %s"%(self.destPath)) 

    def GetFhpg_CSV(self,Code,Name):
        '''
        file format
        .csv
        '''
        try:
            Url1 = 'http://quotes.money.163.com/f10/fhpg_%s.html'%Code
            fhpg =self.GetFhpgBase(Url1,Code)
            if(len(fhpg)>=0):
                columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
                fhpg.to_csv("%s\%s(%s_fhpg).csv"%(self.destPath,Code,Name),index_label=u'序号',columns =columns,encoding='utf_8_sig')
            else:
                print("%s(%s) 分红数据不存在"%(Code,Name))
        except Exception as ex:
            print("%s(%s) 分红数据读取异常"%(Code,Name))

    def GetFhpg(self,Code,Name):
        '''
        file format
        .xls
        '''
        try:
            
            Url1 = 'http://quotes.money.163.com/f10/fhpg_%s.html'%Code
            outFile ="%s\%s(%s_fhpg).xls"%(self.destPath,Code,Name)
            write = pd.ExcelWriter(outFile)
            fhpg =self.GetFhpgBase(Url1,Code)
            if(len(fhpg)>=0):
                columns =['公告日期','分红年度','送股','转增','派息','股权登记日','除权除息日','红股上市日']
                fhpg =fhpg[columns]
                fhpg.to_excel(write,sheet_name='历史分红',index=False)
                write.save() 
            else:
                print("          %s(%s) 分红数据不存在"%(Code,Name))
        except Exception as ex:
            print("           %s(%s) 分红数据读取异常[%s]"%(Code,Name,ex))


    def GetFhpgBase(self,url,code):
        '''
        get FHPG 分红配股
        '''
        getH =RandomHeader()
        headers =getH.GetHeader()
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        dbrow =table0.findAll("tr")
       
        df1 = pd.DataFrame()
       
        dbrow_cnt =len(dbrow)
        col_row =[]
        for k in range(dbrow_cnt):
            if(k<2):
                cells =dbrow[k].findAll("th")
                for cells_col in range(len(cells)):
                    col_name = cells[cells_col].text
                    if(col_name =="分红方案（每10股）"):
                        col_row.append("")
                        col_row.append("")
                        col_row.append("")
                        pass
                    else:
                        if(k==1):
                           col_row[cells_col+2] = col_name
                        else:
                            col_row.append(col_name)
            else:
                cells =dbrow[k].findAll("td")
                data_row =[]
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < lencell:

                        data_row.append(cells[i].text)                                        
                        i=i+1
                    if(len(data_row)>1):    
                        data1=dict(zip(col_row,data_row))
                        row_name ='%d'%(k-2)
                        pds =pd.Series(data1,name =row_name)
                        df1 =df1.append(pds)                   
        data_fh = df1

        # data_fh=data_fh.sort_index()
        # cols =data_fh.columns.values.tolist()
        # for col in cols:
        #     data_fh[col] = data_fh[col].str.replace(',','')
        #     data_fh[col] = data_fh[col].str.replace('--','0')
        # data_fh =data_fh.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        # data_fh.fillna(0,inplace=True)
        return data_fh
    def GetCodeList(self):
        '''
        #获取股票列表
        #code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
        # fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
        ''' 
               
        if os.path.exists("stockListAccount.xls") is True:     #判断文件 stockList.xls 是否存在,如果存在 则从文件中读取
            print("------开始读取stockListAccount股票信息")
            self.df =pd.read_excel('stockListAccount.xls',dtype={'code':'str'})
            self.df =self.df.sort_values(by=['code'])
            self.df =self.df.set_index('code')
            
            print("------结束读取stockListAccount.xls股票信息")
        else:
            self.GetStockListFromNet()#不存在则从网上读取

        return self.df
    def GetStockListFromNet(self):
        print("------开始读取网上股票列表信息")
        self.df = ts.get_stock_basics()             
        self.df =self.df.sort_values(by=['code'])
        write = pd.ExcelWriter('stockListAccount.xls')     #存储到文件  stockList.xls  
        self.df.to_excel(write,index=True)
        write.save()
        print("------结束读取网上股票列表信息")

def MainOpt():
    try:
        opts, args = getopt.getopt(sys.argv[1:],'a:h',['all=','help'])
    except getopt.GetoptError: 
        print(getopt.GetoptError)
        sys.exit()
    all =""
    for o, a in opts:
        if o in ("-h", "--help"):
            print("")
            print("-----命令格式，参照例子:-----------------------------------------------")
            print("|         获取股票列表:")
            print("|                 python ForJerryTaobao.py stock")
            print("|         获取所有股票的分红数据:")
            print("|                 python ForJerryTaobao.py -a a")
            print("|         获取指定股票的分红数据:")
            print("|                 python ForJerryTaobao.py 000651 格力电器")
            print("---------------------------------------------------------------------")
            sys.exit()
        elif o in ("-a", "--all"): #所有股票读取
            all = a
    
    if(all =='a'):

        xlsTest =AccountPd()
        retDf =xlsTest.GetCodeList()
        time_start_total=time.time()
        k=0
        for code in retDf.index:
            # code =retDf.loc[k,'code']
            name = retDf.loc[code,'name'] 
            name =name.replace('*','')
            
            index_k ='序号:%04d'%k
            k =k +1
            print("[%s]开始读取分红数据 %s(%s)"%(index_k,code,name))
            time_start=time.time()
            xlsTest.GetFhpg(code,name)                          #分红
            time_end=time.time()
            time_escape =time_end -time_start
            time.sleep(random.random()+1)
            print("[%s,耗时%s(s)]结束读取分红数据 %s(%s)"%(index_k,time_escape,code,name))
            
        time_end_total=time.time()  
        time_escape_total = time_end_total - time_start_total
        print("共计 耗时%s(s)"%(time_escape_total))  
        
    else:
        code =sys.argv[1]
        xlsTest =AccountPd()
        if(code=='stock'):
            xlsTest.GetStockListFromNet()
        else:
            name =sys.argv[2]
            name =name.replace('*','')
            print("----开始读取 %s(%s)"%(code,name))
            xlsTest.GetFhpg(code,name)                          #分红
            print("----结束读取 %s(%s)"%(code,name))  

if __name__ == '__main__':
    # only for python command - MainOpt()
    MainOpt()
