import pandas as pd
import urllib.request as urllib2
from bs4 import BeautifulSoup 
import datetime
class tradeData:
    def getDataQuaterAndYear(self,userDate):
        user_date = datetime.datetime.strptime(userDate, "%Y-%m-%d")
        season =1
        if user_date.month in [1, 2, 3]:
            season =1
        elif user_date.month in [4,5,6]:
            season =2
        elif user_date.month in [7, 8, 9]:
            season =3
        elif user_date.month in [10, 11, 12]:
            season =4
        return user_date.year,season

    def getDataDayUse(self,fName,Code,startDate,endDate,indexFlag='0'):
        '''
        indexFlag ='0' index data
        indexFlag ='1' stock data
        '''
        #确定起始和结束的日期的年份和季度
        dfResult =pd.DataFrame()
        year,season =self.getDataQuaterAndYear(startDate)
        if(indexFlag=='0'):
            dfResult =self.getIndexDayPart(Code,year,season)
        else:
            dfResult =self.getStockDayPart(Code,year,season)
 
        endDateT = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        while(1):
            month =((season+1)*3)
            if(month>12):
                season =1
                month=3
                year =year+1
            cmpDate =datetime.datetime(year,month,1)
            if(cmpDate<endDateT):
                strDate =cmpDate.strftime("%Y-%m-%d")
                year,season =self.getDataQuaterAndYear(strDate)

                if(indexFlag=='0'):
                    df0 =self.getIndexDayPart(Code,year,season)
                else:
                    df0 =self.getStockDayPart(Code,year,season)

                # df0 =self.getIndexDayPart(Code,year,season)
                if(df0 is None):
                    pass
                else:
                    dfResult =dfResult.append(df0)
            else:
                strDate =cmpDate.strftime("%Y-%m-%d")
                year,season =self.getDataQuaterAndYear(strDate)

                if(indexFlag=='0'):
                    df0 =self.getIndexDayPart(Code,year,season)
                else:
                    df0 =self.getStockDayPart(Code,year,season)

                # df0 =self.getIndexDayPart(Code,year,season)
                if(df0 is None):
                    pass
                else:
                    dfResult =dfResult.append(df0)
                break
        #删除不再开始和结束范围内的数据
        if(dfResult is None):
            return 
        colname_date ='日期'
        dfResult1=dfResult.sort_values(by=[colname_date])
        dfResult1 =dfResult1.reset_index()
        dfResult1 =dfResult1.drop('index',axis =1)
        #改变格式
        startDate =datetime.datetime.strptime(startDate, "%Y-%m-%d")
        strStart =startDate.strftime("%Y%m%d")
        endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        strEnd =endDate.strftime("%Y%m%d")
        dfResult1=dfResult1.drop(dfResult1[colname_date][dfResult1[colname_date]<strStart].index)
        dfResult1=dfResult1.drop(dfResult1[colname_date][dfResult1[colname_date]>strEnd].index)
        
        dfResult1 =dfResult1.reset_index()
        dfResult1 =dfResult1.drop('index',axis =1)
        #将dataframe存入xls文件
        writer = pd.ExcelWriter(fName)
        sheetName =Code
        if(indexFlag=='0'):
            sheetName ="Index"+Code
        dfResult1.to_excel(writer,sheet_name=sheetName)	
        writer.save()   

    def getStockDayPart(self,Code,year,season):  
        '''
        get stock from 163.com
        
        hhttp://quotes.money.163.com/trade/lsjysj_000651.html
        http://quotes.money.163.com/trade/lsjysj_000651.html?year=2019&season=1
        '''
        #判断year和season是不是当前时间,如果是替代url
        now = datetime.datetime.now()
        if((now.year ==year) and (now.month<=(season*3))):
            url ="http://quotes.money.163.com/trade/lsjysj_%s.html"%(Code)
        else:
            url = "http://quotes.money.163.com/trade/lsjysj_%s.html?year=%s&season=%s"%(Code,year,season)
        df0 =self.getDataPart(Code,year,season,url)
        return df0

    def getIndexDayPart(self,indexCode,year,season):  
        '''
        get index from 163.com
        http://quotes.money.163.com/trade/lsjysj_zhishu_000001.html?year=2019&season=1
        http://quotes.money.163.com/trade/lsjysj_zhishu_399001.html
        http://quotes.money.163.com/trade/lsjysj_zhishu_399001.html?year=2019&season=1
        '''
        #判断year和season是不是当前时间,如果是替代url
        now = datetime.datetime.now()
        if((now.year ==year) and (now.month<=(season*3))):
            url ="http://quotes.money.163.com/trade/lsjysj_zhishu_%s.html"%(indexCode)
        else:
            url = "http://quotes.money.163.com/trade/lsjysj_zhishu_%s.html?year=%s&season=%s"%(indexCode,year,season)
        df0 =self.getDataPart(indexCode,year,season,url)
        return df0

    def getDataPart(self,indexCode,year,season,url):
        '''
        '''
        headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6"}
        req = urllib2.Request(url, headers = headers)
        try:
            content = urllib2.urlopen(req).read()
        except:
            return
        soup = BeautifulSoup(content,features="lxml")

        table0 = soup.find("table",{"class":"table_bg001 border_box limit_sale"})
        j=-1
        #read data from 163
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
                    if(j==0):
                        dfContent.append(cells[j].text)
                    else:
                        fNum = cells[j].text.replace(",","")
                        dfContent.append(float(fNum))
                    j =j+1

                dataContent.append(dfContent)
                   
        oneDf =pd.DataFrame(dataContent,columns=colName)
        return oneDf

if __name__ == '__main__':
    test =tradeData()
    test.getDataDayUse("AAAA.xls","000651","2018-03-01","2019-04-28",'1')