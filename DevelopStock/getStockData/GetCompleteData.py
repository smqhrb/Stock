'''
功能说明
来自网上：   1)基本指标(元)  
            2)杜邦分析
            3)行业对比:估值水平, 市场表现 , 财务指标 , 公司规模
            4)资产负债表
            5)利润表
            6)现金流量表
根据三表计算：
            1)偿还能力
            2)竞争力
            3)盈利能力
            4)清算估计
            5)指标
'''
#coding=utf-8
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
import csv
import scipy
import re
import urllib.request as urllib2
import xlwt
from bs4 import BeautifulSoup 
from html.parser import HTMLParser  
from urllib import request
from urllib import parse
from urllib.request import urlopen
#####
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
##### 
class CollectFrom163:
    '''
    从网络读取财务数据 :
            1)资产负债表 利润表 现金流量表
            2)基本指标(元)  
            3)杜邦分析
            4)行业对比:估值水平, 市场表现 , 财务指标 , 公司规模
    计算三表财务数据
            1)偿还能力
            2)竞争力
            3)盈利能力
            4)清算估计
            5)指标
    默认存储目录:.\\Account\\
    '''
    def __init__(self,destPath=".\\Account\\"):
        self.code =""
        self.item =""
        self.filename =""
        self.text =""

        self.wb = xlwt.Workbook()                            #生成xls表
        self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
        self.sheet =self.wsZcfzb
        self.destPath =destPath
        if os.path.exists(self.destPath):                     #检测路径是否存在,不存在则创建路径
            pass
        else:
            os.mkdir(destPath)
        
        
        

    def Get_Stock_List(self):
        '''
        #获取股票列表
        #code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
        # fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
        ''' 
               
        if os.path.exists("stockListAccount.xls") is True:     #判断文件 stockList.xls 是否存在,如果存在 则从文件中读取
            print("------开始读取stockListAccount股票信息")
            self.df =pd.read_excel('stockListAccount.xls',dtype={'code':'str'})
            self.df =self.df.set_index('code')
            print("------结束读取stockListAccount.xls股票信息")
        else:
            print("------开始读取网上股票信息")
            self.df = ts.get_stock_basics()             #不存在则从网上读取
            write = pd.ExcelWriter('stockListAccount.xls')     #存储到文件  stockList.xls  
            self.df.to_excel(write,index=True)
            write.save()
            print("------结束读取网上股票信息")

        return self.df

    def Set_Stock_Code(self,Code):
        self.code =Code

    def Set_Stock_fName(self,filename):
        self.filename =filename

    def Set_Stock_Item(self,item):
        self.item =item

    def Set_Stock_Text(self,text):
        self.text =text

    def Set_Xls_Sheet(self,sheet):
        self.sheet =sheet


           
# 主要抓取函数在下面，要分析数据在网页上的呈现方式进而选择合适的抓取方式。
# 网易股票的资产负债表的应收票据的数据其实被拆成了2张表，第一张表是纯表头，第二张表是纯数据。

    def GetZcfzb(self,url,code):
        '''
        url - 读取链接
        code -股票代码
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")
        #获取财务报表的表头
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j =0
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td") 
            k =len(cells)
            if k<=0:
                cells =row.findAll("th")
                
                self.sheet.write(j, 0, cells[0].text)
                continue
            self.sheet.write(j, 0, cells[0].text)          
        #获取财务报表的数据
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})

        j=0
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            
            if len(cells) > 0:#
                i = 0
                lencell = len(cells)#统计财务报表的年数            
                while i < len(cells):
                    self.sheet.write(j, i+1, cells[i].text)                                        
                    i=i+1
            else:
                cells = row.findAll("th")
                i=0
                while i<len(cells):
                    self.sheet.write(j,i+1,cells[i].text)
                    i=i+1
        return lencell

    #抓取网页数据
    def Get_3_Cell(self,url,code,count,headyear):
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")

        #所以要在第一张表中先找到应收票据的位置。
        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j=-1
        for row in table0.findAll("tr"):
            j+=1
            cells = row.findAll("td")            
            if len(cells) > 0:#
                if cells[0].text.find(self.text)>=0:
                    position = j
                    #print position
                    break;
                
        #然后到第二张表中去抓对应位置的数据。
        lencell=0
        table = soup.find("table",{"class":"table_bg001 border_box limit_sale scr_table"})

        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            if headyear ==0:
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < len(cells):
                        #print cells[i].text
                        self.sheet.write(j, i+1, cells[i].text)                                        
                        i=i+1
                    
        j=-1
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            j+=1
            if j == position:       
                if len(cells) > 0:#
                    i = 0
                    lencell = len(cells)#统计财务报表的年数            
                    while i < len(cells):
                        #print cells[i].text
                        self.sheet.write(count, i+2, cells[i].text)                                        
                        i=i+1
                break
        return lencell

    def GetAllFullAcount(self,df_Code,type='year'):
        '''
        读取所有股票的数据 
        df_code 是存储股票的
        '''
        for Code in df_Code.index:

            Name = df_Code.loc[Code,'name']                     #读取股票的名称
            print(u"-----开始读取:"+Name+"(" + Code +")")
            self.wb = xlwt.Workbook()                           #生成新的xls文件
            self.wsZcfzb = self.wb.add_sheet(u'资产负债表')     #填加 sheet 资产负债表
            self.wsLrb = self.wb.add_sheet(u'利润表')           #填加 sheet 利润表
            self.wsXjllb = self.wb.add_sheet(u'现金流量表')     #填加 sheet 现金流量表
            self.sheet =self.wsZcfzb
            self.GetFullAcount(Code,Name,type)                 #读取数据 并存储
            print(u"-----结束读取:"+Name+"(" + Code +")")
            
    def GetFullAcountTop(self,df_Code,Code,type='year'):
        Name = df_Code.loc[Code,'name']
        print(u"------开始读取:"+Name+"(" + Code +")")
        self.GetFullAcount(Code,Name,type)  
        print(u"------结束读取:"+Name+"(" + Code +")")      


    def GetFullAcount(self,Code,Name,type ='year'):
        '''
        按年度或者报告季读取报表
        code：股票代码
        name: 股票名称
        type: year -按年度读取 ,其他 按报告季节
        '''
        self.sheet = self.wsZcfzb
        #资产负债表
        if type=='year':
            nType ='?type=year'
        else:
            nType=''
        
        Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html%s'%(nType) #资产负债表
        self.GetZcfzb(Url1,Code)

        self.sheet = self.wsLrb
        Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html%s'%(nType) #利润表
        self.GetZcfzb(Url1,Code)

        self.sheet = self.wsXjllb
        Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html%s'%(nType) #现金流量表
        self.GetZcfzb(Url1,Code)

        if len(self.filename)<=0:
            self.wb.save(self.destPath+Name+'('+Code+').xls')
        else:
            self.wb.save(self.destPath+self.filename+'_'+Name+'('+Code+').xls')
        

    def GetData(self,df_Code,count):
        headyear =1
        if (len(self.item)==0 or self.item =='1'):
            self.sheet = self.wsZcfzb             
        elif self.item =='2':
            self.sheet = self.wsLrb
        elif self.item =='3':
            self.sheet = self.wsXjllb
        elif self.item =='4':
            self.sheet = self.wsZcfzb

        for Code in df_Code.index:
            Name = df_Code.loc[Code,'name']
            print(u"股票:"+Name+"(" + Code +") text="+self.text)
            self.sheet.write(count, 0, Code)
            self.sheet.write(count, 1, Name)   
            if (len(self.item)==0 or self.item =='1'):
                Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html?type=year'  
                prefix ='zcfzb_'   
                            
            elif self.item =='2':
                Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html?type=year'
                prefix ='lrb_' 
               
            elif self.item =='3':
                Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html?type=year'
                prefix ='xjllb_'
                
            elif self.item =='4':
                Url1 = 'http://quotes.money.163.com/f10/zycwzb_'+Code+'.html?type=year'
                prefix ='zycwzb_'                 
            LenCell1 = self.Get_3_Cell(Url1,Code,count,headyear)
            count =count+1
        
        self.wb.save(self.destPath +prefix +Code+'.xls')

    def get_industry_classified(self,classify,count):
        print("------开始读取行业%s"%(classify))
        ddf =ts.get_industry_classified()
        ddf1 =ddf.copy()
        a =ddf1[ddf1['c_name'].isin([classify])] 
        headyear =0

        if (len(self.item)==0 or self.item =='1'):
            self.sheet = self.wsZcfzb             
        elif self.item =='2':
             self.sheet = self.wsLrb
        elif self.item =='3':
            self.sheet = self.wsXjllb
        elif self.item =='4':
            self.sheet = self.wsZcfzb
        prefix ='NA_' 
        for ind in a.index:
            Code =a.loc[ind,"code"]
            Name =a.loc[ind,"name"]
            print("------开始读取 Stock="+Name+"("+Code+")")

            self.sheet.write(count, 0, Code)
            self.sheet.write(count, 1, Name)        
            if (len(self.item)==0 or self.item =='1'):
                Url1 = 'http://quotes.money.163.com/f10/zcfzb_'+Code+'.html?type=year'  
                prefix ='zcfzb_'                  
            elif self.item =='2':
                Url1 = 'http://quotes.money.163.com/f10/lrb_'+Code+'.html?type=year'
                prefix ='lrb_' 
            elif self.item =='3':
                Url1 = 'http://quotes.money.163.com/f10/xjllb_'+Code+'.html?type=year'
                prefix ='xjllb_'
            elif self.item =='4':
                Url1 = 'http://quotes.money.163.com/f10/zycwzb_'+Code+'.html?type=year'
                prefix ='zycwzb_'
            
            LenCell1 = self.Get_3_Cell(Url1,Code,count,headyear)
            headyear =1
            print("------结束读取 Stock="+Name+"("+Code+")")
            count =count+1
  
        self.wb.save(self.destPath+prefix+'['+classify+'('+ self.text+')].xls')    
        print("------结束读取行业%s"%(classify))
        # self.GetData(ddf,0)
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


    def getStockBaseInfo(self,stock_code):
        '''
        '''
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        url="http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c"%({'stock_code':stock_code})
        req = request.Request(url=url,headers=headers)
        data = str(urlopen(req).read().decode('GBK'))
        data = data.replace("&nbsp;", "-")
        stock = self.parse_data(data)
        return stock
    def getStockBaseAccount(self,code):
        '''
        paramter :
            code - stock code like '000651'
            fileName - xls name like 'test.xls'
        '''
        stocks = self.getStockBaseInfo(code)
        ret =[]
        for stock in stocks:
            ret.append(stock.getSeries())
        df =pd.DataFrame(ret)
        df.set_index(['日期'],inplace=True)
        df1 =df.T
        # df1.to_excel(fileName) 
        return df1

    def StockValueAssess(self,code,srcFile,outFile):
        '''
        code : stock code
        srcFile: code related file
        outFile: out file

        parameter:
            srcFile: input file of account
            outFile: result for analyst.
        '''
        '''
        
        股票内在价值计算:
            1.资本结构：
                货币资金+应收账款+应收票据>负债总额
                货币资金>负债总额
                投资收益率>利息率
                经营活动现金流>负债总额
                投资性资产(长期股权+交易性金融资产)<经营性资产(总资产-投资性资产)
                预收账款>>预付账款

                不良资产：
                    其他应收款 其他预付款 在建工程
            2.利润分析:
                收入增长速度>成本增长速度
                主营业务>>投资收入+其他业务收入
                盈利能力：
                    投资利润<营业利润
                营业利润/营业资产   投资收益/投资资产
                公司税务变化:
                    营业税及附加  所得税
            3.现金流量表：
                经营活动流入小计 销售收入  --销售应该占大部分
                经营活动净流量同期比
            4.盈利能力：
                ->现金流量表中的销售商品>利润表中的营业收入
                ->经营活动净现金流>营业利润
                ->投资活动产生现金净流量>投资收益*30%
                ->投资活动产生现金净额>负债总额
                ->货币现金+应收账款>负债总额
            5.估值:
                市净率=(市值/(现金+应收票据+投资性房地产))<1.5
                市盈率=(总市值/(企业净利润-投资收益))<15 ,高成长<25
                毛利润率=毛利润/总收入<30%(优秀企业)
        '''
        #read xls 
        print('---------开始读取 %s(%s)'%(srcFile,'资产负债表'))
        zcfzb =pd.read_excel(srcFile,'资产负债表')
        zcfzb.set_index('报告日期', inplace=True)
        cols =zcfzb.columns.values.tolist()
        for col in cols:
            zcfzb[col] = zcfzb[col].str.replace(',','')
            zcfzb[col] = zcfzb[col].str.replace('--','0')
            # zcfzb[col] = zcfzb[col].str.replace('','0')
        zcfzb =zcfzb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        zcfzb.fillna(0,inplace=True)
        print('---------结束读取 %s(%s)'%(srcFile,'资产负债表'))
        # 
        print('---------开始读取 %s(%s)'%(srcFile,'利润表'))
        lrb =pd.read_excel(srcFile,'利润表')
        lrb.set_index('报告日期', inplace=True)
        cols =lrb.columns.values.tolist()
        for col in cols:
            lrb[col] = lrb[col].str.replace(',','')
            lrb[col] = lrb[col].str.replace('--','')
        lrb =lrb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        lrb.fillna(0,inplace=True)
        print('---------结束读取 %s(%s)'%(srcFile,'利润表'))
        #
        print('---------开始读取 %s(%s)'%(srcFile,'现金流量表'))
        xjllb =pd.read_excel(srcFile,'现金流量表')
        xjllb.set_index('报告日期', inplace=True)
        cols =xjllb.columns.values.tolist()
        for col in cols:
            xjllb[col] = xjllb[col].str.replace(',','')
            xjllb[col] = xjllb[col].str.replace('--','')
        xjllb =xjllb.apply(lambda col:pd.to_numeric(col, errors='coerce'))
        xjllb.fillna(0,inplace=True)
        print('---------结束读取 %s(%s)'%(srcFile,'现金流量表'))
        # self.addXlsSheet('002271.xls','result')
        print('---------开始计算三表数据 -------')
        #偿债能力
        fz0 =zcfzb.loc['货币资金(万元)']+zcfzb.loc['应收账款(万元)']+zcfzb.loc['应收票据(万元)'] -zcfzb.loc['流动负债合计(万元)']
        fz1 =zcfzb.loc['货币资金(万元)']-zcfzb.loc['流动负债合计(万元)']
        fz2 =xjllb.loc['经营活动产生的现金流量净额(万元)']/zcfzb.loc['负债合计(万元)']
        fz3 =zcfzb.loc['资产总计(万元)']-2*(zcfzb.loc['长期股权投资(万元)']+zcfzb.loc['交易性金融资产(万元)'])
        fz =pd.DataFrame([fz0,fz1,fz2,fz3],index=['资金加应收减流动负债','货币资金减流动负债合计','经营活动现金/流动负债','经营性资产减投资性资产'])
        #竞争力
        jzl0 =zcfzb.loc['预收账款(万元)']-zcfzb.loc['预付款项(万元)']
        jzl1 =zcfzb.loc['其他应收款(万元)'] 
        jzl4 =zcfzb.loc['在建工程(万元)']
        jzl2 =lrb.loc['营业收入(万元)'] -lrb.loc['营业成本(万元)']
        jzl3 =lrb.loc['营业收入(万元)'] -lrb.loc['投资收益(万元)'] -lrb.loc['其他业务利润(万元)']
        jzl =pd.DataFrame([jzl0,jzl1,jzl4,jzl2,jzl3],['预收减预付','其他应收款','在建工程','净利润','主收入减一次性收入'])
        #盈利能力
        ylnl0 =lrb.loc['营业利润(万元)']-lrb.loc['投资收益(万元)']
        ylnl1 =lrb.loc['营业利润(万元)']/zcfzb.loc['资产总计(万元)']
        ylnl2 =lrb.loc['营业税金及附加(万元)']+lrb.loc['所得税费用(万元)']
        ylnl3 =xjllb.loc['销售商品、提供劳务收到的现金(万元)']/xjllb.loc['经营活动现金流入小计(万元)']
        ylnl4 =xjllb.loc['经营活动产生的现金流量净额(万元)']/lrb.loc['营业利润(万元)']
        ylnl5 =xjllb.loc['购建固定资产、无形资产和其他长期资产所支付的现金(万元)']
        ylnl6 =xjllb.loc['支付的其他与投资活动有关的现金(万元)']
        ylnl =pd.DataFrame([ylnl0,ylnl1,ylnl2,ylnl3,ylnl4,ylnl5,ylnl6],['营业利润减投资收益','利润率','税金','销售/现金流入','现金流量净额/营业利润','对内投资','对外投资'])
        #清算估值
        hbzj =zcfzb.loc['货币资金(万元)']
        yspj =zcfzb.loc['应收票据(万元)']
        yszk =zcfzb.loc['应收账款(万元)']
        ch   =zcfzb.loc['存货(万元)']
        qtldzc =zcfzb.loc['其他流动资产(万元)']
        ldzchj =hbzj +yspj +yszk +ch +qtldzc
        cqgqtz =zcfzb.loc['长期股权投资(万元)']
        gdzcjz =zcfzb.loc['固定资产净值(万元)']
        wxzc =zcfzb.loc['无形资产(万元)']
        qtfldzc =zcfzb.loc['其他非流动资产(万元)']
        fldzchj =cqgqtz +gdzcjz +wxzc +qtfldzc
        zchj =ldzchj +fldzchj
        dqfz =zcfzb.loc['短期借款(万元)']
        yfpj =zcfzb.loc['应付票据(万元)']
        yfzk =zcfzb.loc['应付账款(万元)']
        qtldfz =zcfzb.loc['其他流动负债(万元)']
        ldfzhj =dqfz +yfpj +yfzk +qtldfz
        yfzq =zcfzb.loc['应付债券(万元)']
        cqjk =zcfzb.loc['长期借款(万元)']
        fldfzhj =yfzq +cqjk 
        fzhj =ldfzhj +fldfzhj
        gdqy =zchj -fzhj
        qsgj =pd.DataFrame([hbzj,yspj,yszk,ch,qtldzc,ldzchj,cqgqtz,gdzcjz,wxzc,qtfldzc,fldzchj,zchj,dqfz,yfpj,yfzk,qtldfz,ldfzhj,yfzq,cqjk,fldfzhj,fzhj,gdqy],
                           ['货币资金','应收票据','应收账款','存货','其他流动资产','流动资产合计','长期股权投资','固定资产净值','无形资产','其他非流动资产','非流动资产合计','资产总计','短期借款','应付票据','应付账款','其他流动负债','流动负债合计','应付债券','长期借款','非流动负债合计','负债合计','股东权益'])
        qsgj['清算比率']=[1.0,0.9,0.5,0.7,0.7,0,0.5,0.5,0.8,0.5,0,0,1,1,1,1,0,1,1,0,0,0]
        qsgj['清算后价值%s'%(cols[0])] =qsgj[cols[0]]*qsgj['清算比率']
        qsgj.loc['流动资产合计'] =qsgj.loc['货币资金']+qsgj.loc['应收票据']+qsgj.loc['应收账款']+qsgj.loc['存货']+qsgj.loc['其他流动资产']
        qsgj.loc['非流动资产合计'] =qsgj.loc['长期股权投资']+qsgj.loc['固定资产净值']+qsgj.loc['无形资产']+qsgj.loc['其他非流动资产']
        qsgj.loc['资产总计'] =qsgj.loc['流动资产合计']+qsgj.loc['非流动资产合计']
        qsgj.loc['流动负债合计'] =qsgj.loc['短期借款']+qsgj.loc['应付票据']+qsgj.loc['应付账款']+qsgj.loc['其他流动负债']
        qsgj.loc['非流动负债合计'] =qsgj.loc['应付债券']+qsgj.loc['长期借款']
        qsgj.loc['负债合计'] =qsgj.loc['流动负债合计']+qsgj.loc['非流动负债合计']
        qsgj.loc['股东权益'] =qsgj.loc['资产总计']+qsgj.loc['负债合计']
        qsgj.loc[['流动资产合计','非流动资产合计','资产总计','流动负债合计','非流动负债合计','负债合计','股东权益'],'清算比率']=0
       #
        zbfzl =zcfzb.loc['负债合计(万元)']/zcfzb.loc['资产总计(万元)']#资产负债率
        ldbl =zcfzb.loc['流动资产合计(万元)']/zcfzb.loc['流动负债合计(万元)']#流动比率
        sdbl =(zcfzb.loc['流动资产合计(万元)']-zcfzb.loc['存货(万元)']-zcfzb.loc['预付款项(万元)']-zcfzb.loc['待摊费用(万元)'])/zcfzb.loc['流动负债合计(万元)']#速动比率
        mll =(lrb.loc['营业收入(万元)']-lrb.loc['营业成本(万元)'])/lrb.loc['营业收入(万元)']#毛利率
        jll =lrb.loc['净利润(万元)']/lrb.loc['营业收入(万元)']#净利率
        
        # 存货周转率存货周转率（次数）=销售成本/平均存货余额 
        # 资本周转率:资本周转率=（货币资金+短期投资+应收票据）/长期负债合计×100%
        zbzzl =zcfzb.loc['货币资金(万元)']+zcfzb.loc['应收票据(万元)']/zcfzb.loc['非流动负债合计(万元)']
        # 应收款周转率
        # 净自由现金流:公司自由现金流量(FCFF) =（税后净利润 + 利息费用 + 非现金支出）- 营运资本追加 - 资本性支出
        zjyxjl =lrb.loc['净利润(万元)']+lrb.loc['利息收入(万元)']-lrb.loc['利息支出(万元)']-zcfzb.loc['非流动资产合计(万元)']
        ROE =lrb.loc['净利润(万元)']/zcfzb.loc['所有者权益(或股东权益)合计(万元)']
        ROA =lrb.loc['净利润(万元)']/zcfzb.loc['资产总计(万元)']
        zb =pd.DataFrame([zbfzl,ldbl,sdbl,mll,jll,ROE,ROA],['资产负债率','流动比率','速动比率','毛利率','净利率','ROE','ROA'])
        print('---------结束计算三表数据 -------')
        #    
        write = pd.ExcelWriter(outFile)
        #基本指标(元)
        print('---------开始读取网站 %s[基本指标(元)] -------'%(code))
        jbxx =self.getStockBaseAccount(code)
        print('---------结束读取网站 %s[基本指标(元)] -------'%(code))
        print('---------开始读取网站 %s[杜邦分析]     -------'%(code))
        dbfx =self.getDbfxFrom163(code)
        print('---------结束读取网站 %s[杜邦分析]     -------'%(code))
        print('---------开始读取网站 %s[行业分析]     -------'%(code))
        item,hyfx =self.getHydbFrom163(code)
        print('---------结束读取网站 %s[行业分析]     -------'%(code))
        jbxx.to_excel(write,sheet_name='基本指标(元)',index=True)
        dbfx.to_excel(write,sheet_name='杜邦分析',index=True)
        i =0
        while i<len(hyfx):
            (hyfx[i]).to_excel(write,sheet_name=item[i],index=True)
            i =i+1

        fz.to_excel(write,sheet_name='偿还能力',index=True)
        jzl.to_excel(write,sheet_name='竞争力',index=True)
        ylnl.to_excel(write,sheet_name='盈利能力',index=True)
        qsgj.to_excel(write,sheet_name='清算估计',index=True)
        zb.to_excel(write,sheet_name='指标',index=True)
        write.save() 

    def getHydbFrom163(self,code):
        '''
        from 163 get  行业对比
        '''

        url_hydb_base ='http://quotes.money.163.com/f10/hydb_%s.html#01g02'
        url_hydb =url_hydb_base%(code)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url_hydb, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")

        #获取行业比对 标题
        itemAll = soup.findAll("h2",{"class":"title_01"})
        i =0
        retItem =[]
        while i < len(itemAll):
            retItem.append(itemAll[i].text)
            i =i+1
        ##获取行业比对 的所有表格
        tableAll = soup.findAll("table",{"class":"table_bg001 border_box table_sortable"})
        # print(len(tableAll))
        i =0
        retDf =[]
        while i < len(tableAll):
            table0 =tableAll[i]
            oneDf =pd.DataFrame()
            colName =[]
            dataContent =[]
            for row in table0.findAll("tr"):
                cells = row.findAll("th") #获取表格标题
                if(len(cells)>0):
                    j=0
                    while j <len(cells):
                        colName.append(cells[j].text)
                        j =j+1
                    # print(colName)
                else:
                    cells = row.findAll("td") #获取表格内容
                    j=0
                    dfContent =[]
                    while j <len(cells):
                        # print(cells[j].text)
                        dfContent.append(cells[j].text)
                        j =j+1

                    dataContent.append(dfContent)
                   
            oneDf =pd.DataFrame(dataContent,columns=colName)
            
           
            retDf.append(oneDf)
            i= i+1
        return retItem,retDf #返回表格类别名称 和数据

    def urlOpenContent(self,urlBase,urlfix):
        '''
        parameter:
            url is made by urlBase urlfix
        return content
        '''
        url =urlBase%(urlfix)
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return 
        return content   

    def getDbfxFrom163(self,code):
        '''
        杜邦分析
        parameter 
            code like '000651'
        return DataFrame
        '''
        url_dbfx_base ='http://quotes.money.163.com/f10/dbfx_%s.html#01c08'
        # url_dbfx =url_dbfx_base%('000651')
        content =self.urlOpenContent(url_dbfx_base,'000651')
        soup = BeautifulSoup(content,features="lxml")
        optionAll = soup.findAll("select",{"class":"select01"})  #获取所有日期
        tableAllItem = soup.findAll("td",{"class":"dbbg01"}) #获取所有的项目名称
        i=0
        item =[]
        while i<len(tableAllItem):
            item.append(tableAllItem[i].text)
            i = i+1
        dfRet =pd.DataFrame(columns=item) #根据项目名称生成列名字
        urlOptionBase ="http://quotes.money.163.com/f10/dbfx_000651.html?date=%s#01c08"
        k =0
        while k <len(optionAll[0].contents):
            
            if optionAll[0].contents[k].name=='option':
                optionValue =optionAll[0].contents[k]['value']
                # urlOption =urlOptionBase%optionValue
                content =self.urlOpenContent(urlOptionBase,optionValue)
                soup = BeautifulSoup(content,features="lxml")
                tableAllValue = soup.findAll("td",{"class":"dbbg02"})#读取每年度的数据
                dataRow =[]
                indexJ =0
                while indexJ < len(tableAllValue):
                    dataRow.append(tableAllValue[indexJ].text) 
                    indexJ =indexJ+1
                dfRet.loc[optionValue]=dataRow
            k = k+1
        
        return dfRet

    def CaculateAssest(self,filePath=None):
        '''
        股票代码从文件中读取 文件的名字(在括号之间读取股票代码),例如：
                                  test_长安汽车(000625).xls
                                  
        分析结果生成新的文件名字,例如：Atest_长安汽车(000625).xls
        '''
        if filePath is None:
            filePath =self.destPath
        pathDir =  os.listdir(filePath) #从目录中读取文件名字
        codeList =[]
        fnameList =[]
        for allDir in pathDir:
            child = os.path.join('%s\%s' % (filePath, allDir))
            if os.path.isfile(child):
                child =child[child.rfind("\\")+1:]
                if(child.rfind(")")>0):
                    name = child[child.rfind("(")+1:child.rfind(")")]#查找位于股票直接的代码
                    if(len(name)>0):
                        codeList.append(name)
                        fnameList.append(child)
                else:
                    continue
        
        for code,name in zip(codeList,fnameList):
            print("read from %s,write to %s"%(filePath +name,filePath+"\\"+'A'+name))#分析结果的名字 
            self.StockValueAssess(code,filePath +name,filePath+"\\"+'A'+name)


#主函数 

if __name__ == '__main__':
    Test =CollectFrom163()  
    Test.CaculateAssest()  
    # Test.Set_Stock_fName("test") 
    # Test.Set_Stock_Item("3")
    # Test.Set_Stock_Text("现金及现金等价物净增加额(万元)")
    # kk = ts.get_industry_classified()
    # print(kk)
    # # df = Test.Get_Stock_List()
    # # count = 1
    # # Test.GetFullAcount('601319')n
    # Test.get_industry_classified('家电行业',1)


    # stocks = Test.getStockBaseInfo("002122")
    # Test.getStockBaseAccount("000651")
    # Test.StockValueAssess('000651','000651.xls','A000651.xls')
    # Test.getDbfxFrom163('002122')
    # item,hyfx =Test.getHydbFrom163('000651')
    # i =0
    # while i<len(hyfx):
    #     print(item[i])
    #     print(hyfx[i])
    #     i =i+1
    # ret =[]
    # for stock in stocks:
    #     print (stock)
    #     ret.append(stock.getSeries())
    # df =pd.DataFrame(ret)
    # df.set_index(['日期'],inplace=True)
    # print(df)
    # df1 =df.T
   
    # df1.to_excel('test.xls')