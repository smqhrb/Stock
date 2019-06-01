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
    获取财务数据 to csv
    pandas 
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

    def GetFullAcount(self,Code,Name,typeQ ='year'):
        '''
        按年度或者报告季读取报表
        code：股票代码
        name: 股票名称
        typeQ: year -按年度读取 ,其他 按报告季节
        '''
        # self.sheet = self.wsZcfzb
        #资产负债表
        if typeQ=='year':
            nType ='?type=year'
        else:
            nType=''
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html%s'%(nType) #资产负债表
        zcfzb =self.GetZcfzb(Url1,Code)
       

        # self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html%s'%(nType) #利润表
        lrb =self.GetZcfzb(Url1,Code)

        # self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html%s'%(nType) #现金流量表
        llb =self.GetZcfzb(Url1,Code)
        # Name =Name.replace('*', '')
        # if len(self.filename)<=0:
        #     self.wb.save(self.destPath+Name+'('+Code+').csv')
        # else:
        #     self.wb.save(self.destPath+self.filename+'_'+Name+'('+Code+').csv')
        
        # zcfzb.to_excel("%s\%s(%s_%s_zcfzb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # lrb.to_excel("%s\%s(%s_%s_lrb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        # llb.to_excel("%s\%s(%s_%s_llb).xlsx"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期')
        zcfzb.to_csv("%s\%s(%s_%s_zcfzb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        lrb.to_csv("%s\%s(%s_%s_lrb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
        llb.to_csv("%s\%s(%s_%s_llb).csv"%(self.destPath,Code,Name,typeQ),index_label=u'报告日期',encoding='utf_8_sig')
 
    def GetZcfzb(self,url,code):
        '''
        url - 读取链接
        code -股票代码
        '''
        # headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
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
        j =0
        df = pd.DataFrame()
        data0 =[]
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td") 
            k =len(cells)
            if k<=0:
                cells =row.findAll("th")
                
                # self.sheet.write(j, 0, cells[0].text)
                data0.append(cells[0].text)
                continue
            # self.sheet.write(j, 0, cells[0].text)  
            data0.append(cells[0].text)   
        # df =df.append(data0)   
        # print(df) 
        #获取财务报表的数据
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})
        df1 = pd.DataFrame()
        col_row=[]
        
        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            data_row =[]
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    # self.sheet.write(j, i+1, cells[i].text)
                    data_row.append(cells[i].text)                                        
                    i=i+1
                # df1 =df1.append(data1)
                if(len(data_row)>1):    
                    data1=dict(zip(col_row,data_row))
                    pds =pd.Series(data1,name =data0[j-1])
                    df1 =df1.append(pds)   
            else:
                cells = row.findAll("th")
                i=0
                while i<len(cells):
                    # self.sheet.write(j,i+1,cells[i].text)
                    col_row.append(cells[i].text)  
                    i=i+1

        zcfzb = df1.T
        # zcfzb.set_index('报告日期', inplace=True)
        zcfzb=zcfzb.sort_index()
        cols =zcfzb.columns.values.tolist()
        for col in cols:
            zcfzb[col] = zcfzb[col].str.replace(',','')
            zcfzb[col] = zcfzb[col].str.replace('--','0')
        zcfzb =zcfzb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        zcfzb.fillna(0,inplace=True)
        return zcfzb

    def GetCodeList(self):
        try:
            print("------开始读取股票基本信息.....")
            ddf =ts.get_stock_basics()
            ddf =ddf.sort_index()

            ddf.to_csv('%s\StockClass.csv'%(self.destPath),encoding='utf_8_sig')
            print("------结束读取股票基本信息.....")
        except Exception as ex:
            print("------读取股票失败.....")
            pass
    def getBaseAccountToCSV(self,code,name):
        '''
        main function to read jbxx of account
        '''
        # print('---------开始读取 %s[基本指标(元)] -------'%(code))
        jbxx =self.getStockBaseAccount(code)
        # print('---------结束读取 %s[基本指标(元)] -------'%(code)) 
        jbxx.to_csv('%s\%s(%s)_jbxx.csv'%(self.destPath,code,name),encoding='utf_8_sig')

    def getStockBaseAccount(self,code):
        '''
        paramter :
            code - stock code like '000651'
            
        '''
        stocks = self.getStockBaseInfo(code)
        ret =[]
        for stock in stocks:
            ret.append(stock.getSeries())
        df =pd.DataFrame(ret)
        df.set_index(['日期'],inplace=True)
        # df1 =df.T

        return df

    def getStockBaseInfo(self,stock_code):
        '''
        '''
        # headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        getH =RandomHeader()
        headers =getH.GetHeader()
        url="http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c"%({'stock_code':stock_code})
        req = urllib2.Request(url=url,headers=headers)
        data = str(urllib2.urlopen(req).read().decode('GBK'))
        data = data.replace("&nbsp;", "-")
        stock = self.parse_data(data)
        return stock
    def parse_data(self,urldata):
        '''
        日期,每股净资产,每股收益,每股现金含量,每股资本公积金,固定资产合计,流动资产合计,资产总计,
        长期负债合计,主营业务收入,财务费用,净利润 
        '''
        tp = stock_parser()
        tp.feed(urldata)
        data = tp.data
        i = 0
        arr = []
        stocks = []
        for row in data:
            arr.append(row.replace(",","").replace("元","").replace("\r\n",""))
            i += 1
            if i%22 ==0 and i>0:
                line = ",".join(arr)
                stock = StockAccountBaseInfo(line)
                stocks.append(stock)
                arr = []
        return stocks

class StockAccountBaseInfo:
    '''
    构建股票财务基本信息字符串
    '''
    def __init__(self,line):
        # 20011231,每股净资产,1.5727,每股收益,0.3438,每股现金含量,11,每股资本公积金,0.5289,
        # 固定资产合计,11,流动资产合计,11,资产总计,11,长期负债合计,16,主营业务收入,11,11,净利润,11
        arr = line.split(",")
        self.day = arr[0].replace("-","") if arr[0]!='-' else '0'   #日期
        self.mgzjc = arr[2] if arr[2]!='-' else '0'                 #每股净资产
        self.mgsy = arr[4] if arr[4]!='-' else '0'                  #每股收益
        self.mgxjhl = arr[6] if arr[6]!='-' else '0'                #每股现金含量                
        self.mgjbgjj = arr[8] if arr[8]!='-' else '0'               #每股资本公积金
        self.gdzchj = arr[10] if arr[10]!='-' else '0'              #固定资产合计
        self.ldzchj = arr[12] if arr[12]!='-' else '0'              #流动资产合计
        self.zchj = arr[14] if arr[14]!='-' else '0'                #资产总计                
        self.cqfzhj = arr[16] if arr[16]!='-' else '0'              #长期负债合计
        self.zyywsr = arr[18] if arr[18]!='-' else '0'              #主营业务收入
        self.cwfy = arr[19] if arr[19]!='-' else '0'                #财务费用
        self.jlr = arr[21] if arr[21]!='-' else '0'                 #净利润
        self.series =pd.Series({'日期':self.day,'每股净资产':self.mgzjc,'每股收益':self.mgsy,'每股现金含量':self.mgxjhl,'每股资本公积金':self.mgjbgjj,'固定资产合计':self.gdzchj,
                     '流动资产合计':self.ldzchj,'资产总计':self.zchj,'长期负债合计':self.cqfzhj,'主营业务收入':self.zyywsr,'财务费用':self.cwfy,'净利润':self.jlr})
    def getSeries(self):
        return self.series    


    def __repr__(self):
        # return """day:%s,mgzjc:%s,mgsy:%s,mgxjhl:%s,mgjbgjj:%s,gdzchj:%s,ldzchj:%s,zchj:%s,
        # cqfzhj:%s,zyywsr:%s,cwfy:%s,jlr:%s"""%(self.day,self.mgzjc,self.mgsy,self.mgxjhl,
        #                                        self.mgjbgjj,self.gdzchj,self.ldzchj,self.zchj,
        #                                        self.cqfzhj,self.zyywsr,self.cwfy,self.jlr)
        return """日期:%s,每股净资产:%s,每股收益:%s,每股现金含量:%s,每股资本公积金:%s,固定资产合计:%s,流动资产合计:%s,资产总计:%s,
        长期负债合计:%s,主营业务收入:%s,财务费用:%s,净利润:%s"""%(self.day,self.mgzjc,self.mgsy,self.mgxjhl,
                                               self.mgjbgjj,self.gdzchj,self.ldzchj,self.zchj,
                                               self.cqfzhj,self.zyywsr,self.cwfy,self.jlr)        

class stock_parser(HTMLParser):
    '''
    解析网络响应 -读取财务基本信息
    '''
    def __init__(self):
        HTMLParser.__init__(self)
        self.handledtags = ['td']
        self.processing = None
        self.data = []

    def handle_starttag(self,tag,attrs):
        if tag in self.handledtags and len(attrs)>0 and attrs[0][0]=='align':
            self.processing = tag

    def handle_data(self,data):
        if self.processing:
            self.data.append(data)

    def handle_endtag(self,tag):
        if tag == self.processing:
            self.processing = None

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
            print("|                 python DnAcountDt.py stock")
            print("|         获取所有股票的财务数据:")
            print("|                 python DnAcountDt.py -a a")
            print("|         获取指定股票的财务数据:")
            print("|                 python DnAcountDt.py 000625 格力电器")
            print("---------------------------------------------------------------------")
            sys.exit()
        elif o in ("-a", "--all"): #所有股票读取
            all = a

    if(all =='a'):

        xlsTest =AccountPd()
        retDf =pd.read_csv("%s\StockClass.csv"%xlsTest.destPath)
        time_start_total=time.time()
        for k in range(len(retDf)):
            code =retDf.loc[k,'code']
            name =retDf.loc[k,'name']
            name =name.replace('*','')
            code ='%06d'%code
            index_k ='序号:%04d'%k
            
            print("[%s]开始读取 %s(%s)"%(index_k,code,name))
            time_start=time.time()
            xlsTest.GetFullAcount(code,name,typeQ='year')
            xlsTest.GetFullAcount(code,name,typeQ='quarter')
            xlsTest.getBaseAccountToCSV(code,name)
            time_end=time.time()
            time_escape =time_end -time_start
            print("[%s,耗时%s(s)]结束读取 %s(%s)"%(index_k,time_escape,code,name))
            break
        time_end_total=time.time()  
        time_escape_total = time_end_total - time_start_total
        print("共计 耗时%s(s)"%(time_escape_total))  
        
    else:
        code =sys.argv[1]
        xlsTest =AccountPd()
        if(code=='stock'):
            xlsTest.GetCodeList()
        else:
            name =sys.argv[2]
            name =name.replace('*','')
            print("----开始读取 %s(%s)"%(code,name))
            xlsTest.GetFullAcount(code,name,typeQ='year')
            xlsTest.GetFullAcount(code,name,typeQ='quarter') 
            xlsTest.getBaseAccountToCSV(code,name)
            print("----结束读取 %s(%s)"%(code,name))  

if __name__ == '__main__':
    # only for python command - MainOpt()
    MainOpt()

    

