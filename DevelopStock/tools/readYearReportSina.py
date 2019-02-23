# from  xml.dom import  minidom
# import xlwt
# import os,shutil
# import time,urllib2
# def Xmltoxls(xmlname,xlsname):
#     if os.path.getsize(xmlname)<1024:
#         return False
#     wb=xlwt.Workbook(encoding='utf-8')
#     ws=wb.add_sheet('Table')
#     fp_xml=minidom.parse(xmlname)
#     root=fp_xml.documentElement
#     Row=root.getElementsByTagName('Row')
#     Data=root.getElementsByTagName('Data')
#     col_num=len(Data)/len(Row)
#     row_num= 0
#     for row in Row:
#         Data=row.getElementsByTagName('Data')
#         for i in range(col_num):
#             if len(Data[i].childNodes)==0:
#                 ws.write(row_num,i,' ')
#                 continue
#             ws.write(row_num,i,Data[i].childNodes[0].nodeValue.strip().encode('utf-8'))
#         row_num+=1
#     wb.save(xlsname)
#     return True
# def xml_Error_C(filename):
#     fp_xml=open(filename)
#     fp_x=''#中文乱码改正
#     for i in range(os.path.getsize(filename)):
#         i+=1
#         a=fp_xml.read(1)
#         if a=='&':
#             fp_xml.seek(-1,1)
#             if fp_xml.read(6)=='&nbsp;':
#                 i+=5
#                 continue
#             else:
#                 fp_xml.seek(-5,1)
#         fp_x+=a
#     fp_xml=open(filename,'w+')
#     fp_xml.write(fp_x)
#     fp_xml.flush()
#     fp_xml.close()
# def errorlog(error):
#     fp_error=open('errorlog.txt','a')
#     fp_error.write(error+'\n')
#     fp_error.close
# fp_code=open('stockcode..txt')
# fp_basic=open('basicdata_url.txt')
# temp='z:\\temp.xml'
# for line in fp_code:#设置代码起始位置
#     if line.split()[0]=='601958':
#         break
# for line in fp_code:#遍历所有代码及名称
#     filepath='basicdata\\'+line.split()[0]+line.split()[1].replace('*','&')#建立文件夹
#     if not os.path.isdir(filepath):
#         os.makedirs(filepath)
#     for url in fp_basic:#抓取所有数据并保存
#         url_f=url.split()[0]+line.split()[0]+('01' if int(line.split()[0])>599999 else '02')+'&exp=1'
#         print ('I am handle '+line+' '+url.split()[1]+' '+'data for you')
#         filename=filepath+'\\'+line.split()[0]+' '+url.split()[1]+'.xls'
#         while True:#get xml data
#             try:
#                 u=urllib2.urlopen(url_f)
#                 time.sleep(0.3)
#                 data=u.read()
#                 f=open(temp,'w+')#保存文件
#                 f.write(data)
#                 f.flush()
#                 f.close()
#                 break
#             except :
#                 print ('Network error,try latter!')
#                 time.sleep(10)
#         while True:#xml data to xls data
#             if url.split()[1] in ['News','Notice','Subject']:
#                 shutil.move(temp,filename) #   os.rename("oldname","newname")
#                 break
#             try:            
#                 xml_Error_C(temp)
#                 Xmltoxls(temp,filename)
#             except IOError:
#                 errorlog('No '+filename)
#             except:
#                 shutil.move(temp,filename)
#                 errorlog('Not Done '+filename)
#             break
#         time.sleep(0.2)
#     time.sleep(7)
#     fp_basic.seek(0)
# print ('All data have been getted.')
# fp_code.close()
# fp_basic.close()


###############
# coding=utf-8
from html.parser import HTMLParser  

from urllib import request
from urllib import parse
from urllib.request import urlopen
import sys

type = sys.getfilesystemencoding()
# 截止日期
# 每股净资产
# 每股收益
# 每股现金含量
# 每股资本公积金
# 固定资产合计
# 流动资产合计
# 资产总计
# 长期负债合计
# 主营业务收入
# 财务费用
# 净利润
class Stock:
    def __init__(self,line):
        # 20011231,每股净资产,1.5727,每股收益,0.3438,每股现金含量,11,每股资本公积金,0.5289,
        # 固定资产合计,11,流动资产合计,11,资产总计,11,长期负债合计,16,主营业务收入,11,11,净利润,11
        arr = line.split(",")
        self.day = arr[0].replace("-","") if arr[0]!='-' else '0'
        self.mgzjc = arr[2] if arr[2]!='-' else '0'
        self.mgsy = arr[4] if arr[4]!='-' else '0'
        self.mgxjhl = arr[6] if arr[6]!='-' else '0'
        self.mgjbgjj = arr[8] if arr[8]!='-' else '0'
        self.gdzchj = arr[10] if arr[10]!='-' else '0'
        self.ldzchj = arr[12] if arr[12]!='-' else '0'
        self.zchj = arr[14] if arr[14]!='-' else '0'
        self.cqfzhj = arr[16] if arr[16]!='-' else '0'
        self.zyywsr = arr[18] if arr[18]!='-' else '0'
        self.cwfy = arr[19] if arr[19]!='-' else '0'
        self.jlr = arr[21] if arr[21]!='-' else '0'


    def __repr__(self):
        return """day:%s,mgzjc:%s,mgsy:%s,mgxjhl:%s,mgjbgjj:%s,gdzchj:%s,ldzchj:%s,zchj:%s,
        cqfzhj:%s,zyywsr:%s,cwfy:%s,jlr:%s"""%(self.day,self.mgzjc,self.mgsy,self.mgxjhl,
                                               self.mgjbgjj,self.gdzchj,self.ldzchj,self.zchj,
                                               self.cqfzhj,self.zyywsr,self.cwfy,self.jlr)

class stock_parser(HTMLParser):
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

def parse_data(urldata):
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
            stock = Stock(line)
            stocks.append(stock)
            arr = []
    return stocks


def get_stock(stock_code):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
    url="http://vip.stock.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/%(stock_code)s.phtml?qq-pf-to=pcqq.c2c"%({'stock_code':stock_code})
    req = request.Request(url=url,headers=headers)
    data = str(urlopen(req).read().decode('GBK'))
    data = data.replace("&nbsp;", "-")
    stocks = parse_data(data)
    return stocks

if __name__ == '__main__':

    stocks = get_stock("002122")
    for stock in stocks:
        print (stock)
