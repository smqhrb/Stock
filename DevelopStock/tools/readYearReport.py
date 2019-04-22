
'''
down load year report 
'''
import urllib.request 
import urllib
import re 
import os 
import pandas as pd
URL_YEAR_BASE ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/ndbg.phtml'#
URL_HALFYEAR_BASE ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/zqbg.phtml'#
URL_Q1_BASE ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/yjdbg.phtml'
URL_Q3_BASE ='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/%s/page_type/sjdbg.phtml'
TARGET_URL='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=%s%s'
class ReportDownSina:
    '''
    this for report down load 
    '''
    def __init__(self,stockList):
        self.stockList =stockList
    def readStockListFromTxt(self,filename):
        '''
        add stock in the txt file like this
        000651
        000652
        return list
        '''
        f=open(filename) #'stock_num.txt'
        stock = [] 
        for line in f.readlines(): 
            line = line.replace('\n','') 
            stock.append(line) 
        self.stockList =stock
        f.close() 
        return stock

    def readStockListFromXls(self,filename,colName='ts_code',suffix='1'):
        '''
        parameter is file name,stock column name ,suffix ='1' remove suffix or '0' keep suffix

        return list
        '''
        stockList =pd.read_excel(filename)
        rlist =stockList[colName].tolist()
        rlist =self.listRemoveDup(rlist)

        returnList =[]
        if(suffix=='1'):
            for each in rlist:
                returnList.append(each.split('.')[0])
        else:
            returnList =rlist
        print(returnList)
        self.stockList =returnList
        return returnList

    def listRemoveDup(self,inList):
        newList =[]
        for id in inList:
            if id not in newList:
                id= "%06d"%(id)
                newList.append(id)
        return newList
    def reportDownByStock(self,url,each,baseDir):
        req = urllib.request.Request(url) 
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
        page = urllib.request.urlopen(req) 
        try: 
            html = page.read().decode('gbk') 
            target = r'&id=[_0-9_]{7}' 
            target_list = re.findall(target,html) 

            if(os.path.exists(baseDir+'/'+each)):
                pass
            else:
                os.mkdir(baseDir+'/'+each) 
            sid = each 
            #print(target_list)
                
            for each in target_list: 
                #print(a) #print(each) 

                target_url=TARGET_URL%(sid,each) 
                #print(target_url) 
                treq = urllib.request.Request(target_url) 
                #'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'

                # treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
                treq.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6') 
                tpage = urllib.request.urlopen(treq) 
                try: 
                    thtml = tpage.read().decode('gbk') 
                    #print(thtml) 
                    file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml) 
                    try: 
                        #print(file_url.group(0)) 
                        local = baseDir+'/'+sid+'/'+file_url.group(0).split("/")[-2]+'.pdf' 
                        #调试用作文件占位 
                        # #open(local, 'wb').write(b'success') 
                        #print(local) 
                        print(file_url.group(0))
                        urllib.request.urlretrieve(file_url.group(0),local,None) 
                    except Exception as e: 
                        # print('PDF is not available;'+target_url) 
                            # print ('str(Exception):\t', str(Exception))
                            # print ('str(e):\t\t', str(e))
                            print ('repr(e):\t', repr(e))
                            # print ('e.message:\t', e.message)
                            # print ('traceback.print_exc():'+traceback.print_exc())
                            # print ('traceback.format_exc():\n%s' % traceback.format_exc())
                except Exception as e: 
                    print('page of report  error:'+target_url)
                    print ('repr(e):\t', repr(e)) 
        except Exception as e: 
            print('year report list error: '+url)
            print ('repr(e):\t', repr(e))

    def reportDown(self,targetDir='YearReport',type='y'):
        '''
        parameter: 
            'y'-year report;
            'hf'- half year report
            'q1' -quarter 1 report
            'q3' -quarter 3 report

        '''
        baseDir = './'+targetDir
        if(os.path.exists(baseDir)):
            pass
        else:
            os.mkdir(baseDir) 
        
        urlBase =URL_YEAR_BASE
        if(type=='y'):
            urlBase =URL_YEAR_BASE
        if(type=='hy'):
            urlBase =URL_HALFYEAR_BASE
        if(type=='q1'):
            urlBase =URL_Q1_BASE
        if(type=='q3'):
            urlBase =URL_Q3_BASE
        reachCount =0
        for each in self.stockList: 
            reachCount =reachCount +1
            print('%d:%s;'%(reachCount,each))
            url=urlBase%each 
            self.reportDownByStock(url,each,baseDir)
 
    def login(self,username,password):
        # import urllib
        # from urllib import parse
        # data=parse.urlencode({'username':username,
        #                     'password':password,
        #                     'continue':'http://www.verycd.com/',
        #                     'login_submit':u'登录'.encode('utf-8'),
        #                     'save_cookie':1,})
        # url = 'http://www.verycd.com/signin'
        # # self.opener.open(url,data).read()
        
        # postdata=parse.urlencode({
        #     'username':'XXXXX',
        #     'password':'XXXXX',
        #     'continueURI':'http://www.verycd.com/',
        #     'fk':fk,
        #     'login_submit':'登录'
        # })
        # req = urllib.request.Request(
        #     url = 'http://secure.verycd.com/signin/*/http://www.verycd.com/',
        #     data = postdata
        # )
        # result = urllib.request.urlopen(req).read()

        from urllib import request
        from urllib import parse
        from urllib.request import urlopen

        values = {'username': '962457839@qq.com', 'password': 'XXXX'}
        data = parse.urlencode(values).encode('utf-8')  # 提交类型不能为str，需要为byte类型
        url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
        request = request.Request(url, data)
        response = urlopen(request)
        print(response.read().decode())

if __name__ == '__main__':
    rlist =[]
    aa =ReportDownSina(rlist)
    # rlist =aa.readStockListFromXls('hs300.xls','code','0')
    rlist =aa.readStockListFromTxt('stock_num.txt')
    aa.reportDown(type='q1')
    aa.reportDown(type='q3')
# ###################
# from threading import Thread
# from Queue import Queue
# from time import sleep
# #q是任务队列
# #NUM是并发线程总数
# #JOBS是有多少任务
# q = Queue()
# NUM = 2
# JOBS = 10
# #具体的处理函数，负责处理单个任务
# def do_somthing_using(arguments):
#     print (arguments)
# #这个是工作进程，负责不断从队列取数据并处理
# def working():
#     while True:
#         arguments = q.get()
#         do_somthing_using(arguments)
#         sleep(1)
#         q.task_done()
# #fork NUM个线程等待队列
# for i in range(NUM):
#     t = Thread(target=working)
#     t.setDaemon(True)
#     t.start()
# #把JOBS排入队列
# for i in range(JOBS):
#     q.put(i)
# #等待所有JOBS完成
# q.join()
# ###################


# f=open('stock_num.txt') 
# stock = [] 
# for line in f.readlines(): 
#     #print(line,end = '') 
#     line = line.replace('\n','') 
#     stock.append(line) 
#     #print(stock) 
# f.close() 
# print(stock) 
# for each in stock: 
#     url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+each+'/page_type/ndbg.phtml' 
#     req = urllib.request.Request(url) 
#     req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
#     page = urllib.request.urlopen(req) 
#     try: 
#         html = page.read().decode('gbk') 
#         target = r'&id=[_0-9_]{7}' 
#         target_list = re.findall(target,html) 
#         os.mkdir('./'+each) 
#         sid = each 
#         #print(target_list) 
#         for each in target_list: 
#             #print(a) #print(each) 
#             target_url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid='+sid+each 
#             #print(target_url) 
#             treq = urllib.request.Request(target_url) 
#             treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
#             tpage = urllib.request.urlopen(treq) 
#             try: 
#                 thtml = tpage.read().decode('gbk') 
#                 #print(thtml) 
#                 file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml) 
#                 try: 
#                     #print(file_url.group(0)) 
#                     local = './'+sid+'/'+file_url.group(0).split("/")[-2]+'.pdf' 
#                     #调试用作文件占位 
#                     # #open(local, 'wb').write(b'success') 
#                     #print(local) 
#                     urllib.request.urlretrieve(file_url.group(0),local,None) 
#                 except: 
#                     print('PDF失效;'+target_url) 
#             except: 
#                 print('年报下载页面编码错误;'+target_url) 
#     except: 
#         print('年报列表页面编码错误;'+url)


# coding = UTF-8
# 爬取自己编写的html链接中的PDF文档,网址：file:///E:/ZjuTH/Documents/pythonCode/pythontest.html

# import urllib.request
# import re
# import os

# # open the url and read
# def getHtml(url):
#     page = urllib.request.urlopen(url)
#     html = page.read()
#     page.close()
#     return html

# # compile the regular expressions and find
# # all stuff we need
# def getUrl(html):
#     reg = r'([A-Z]\d+)' #匹配了G176200001
#     url_re = re.compile(reg)
#     url_lst = url_re.findall(html.decode('UTF-8')) #返回匹配的数组
#     return(url_lst)

# def getFile(url):
#     file_name = url.split('/')[-1]
#     u = urllib.request.urlopen(url)
#     f = open(file_name, 'wb')

#     block_sz = 8192
#     while True:
#         buffer = u.read(block_sz)
#         if not buffer:
#             break

#         f.write(buffer)
#     f.close()
#     print ("Sucessful to download" + " " + file_name)


# root_url = 'http://pm.zjsti.gov.cn/tempublicfiles/'  #下载地址中相同的部分

# raw_url = 'file:///E:/ZjuTH/Documents/pythonCode/pythontest.html'

# html = getHtml(raw_url)
# url_lst = getUrl(html)

# os.mkdir('pdf_download')
# os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

# for url in url_lst[:]:
#     url = root_url + url+'/'+url+'.pdf'  #形成完整的下载地址
    # getFile(url)