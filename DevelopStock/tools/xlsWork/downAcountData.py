#coding=utf-8
import getopt
import tushare as ts
import numpy as np
import pandas as pd
import os,time,sys,re,datetime
# import csv
# import scipy
# import re
import urllib.request as urllib2
# import xlwt
from bs4 import BeautifulSoup 
# from html.parser import HTMLParser  
# from urllib import request
# from urllib import parse
# from urllib.request import urlopen

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

        # self.wb = xlwt.Workbook()                            #生成xls表
        # self.wsZcfzb = self.wb.add_sheet(u'资产负债表')       #填加 资产负债表 
        # self.wsLrb = self.wb.add_sheet(u'利润表')             #填加 利润表 
        # self.wsXjllb = self.wb.add_sheet(u'现金流量表')       #填加 现金流量表 
        # self.sheet =self.wsZcfzb
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

def main():
    print(sys.argv[0])
    print(sys.argv[1])
    print(sys.argv[2]) 

    destPath ="%s\\Account"%(sys.argv[1]) 
    xlsTest =AccountPd(destPath=destPath)
    code =sys.argv[2]

    if(code=='stock'):
        xlsTest.GetCodeList()
    else:
        print(sys.argv[3]) 
        name =sys.argv[3]
        xlsTest.GetFullAcount(code,name,typeQ='year')
        xlsTest.GetFullAcount(code,name,typeQ='quarter')
    
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
            print("|                 python downAcountData.py stock")
            print("|         获取所有股票的财务数据:")
            print("|                 python downAcountData.py -a a")
            print("|         获取指定股票的财务数据:")
            print("|                 python downAcountData.py 000625 格力电器")
            print("---------------------------------------------------------------------")
            sys.exit()
        elif o in ("-a", "--all"): #所有股票读取
            all = a
    print("kk%s"%all)
    if(all =='a'):
        xlsTest =AccountPd()
        retDf =pd.read_csv("%s\StockClass.csv"%xlsTest.destPath)
        for k in range(len(retDf)):
            code =retDf.loc[k,'code']
            name =retDf.loc[k,'name']
            code ='%06d'%code
            print("[%d]开始读取 %s(%s)"%(k,code,name))
            xlsTest.GetFullAcount(code,name,typeQ='year')
            xlsTest.GetFullAcount(code,name,typeQ='quarter')
            print("[%d]结束读取 %s(%s)"%(k,code,name))
    else:
        code =sys.argv[1]
        xlsTest =AccountPd()
        if(code=='stock'):
            xlsTest.GetCodeList()
        else:
            name =sys.argv[2]
            print("----开始读取 %s(%s)"%(code,name))
            xlsTest.GetFullAcount(code,name,typeQ='year')
            xlsTest.GetFullAcount(code,name,typeQ='quarter') 
            print("----结束读取 %s(%s)"%(code,name))  

if __name__ == '__main__':
    # work with AcountWork.xlsm -main()
    main()
    # only for python command - MainOpt()
    # MainOpt()

