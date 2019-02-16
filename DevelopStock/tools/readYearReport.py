# coding = UTF-8
# 爬取自己编写的html链接中的PDF文档,网址：file:///E:/ZjuTH/Documents/pythonCode/pythontest.html

import urllib.request
import re
import os

# open the url and read
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    page.close()
    return html

# compile the regular expressions and find
# all stuff we need
def getUrl(html):
    reg = r'([A-Z]\d+)' #匹配了G176200001
    url_re = re.compile(reg)
    url_lst = url_re.findall(html.decode('UTF-8')) #返回匹配的数组
    return(url_lst)

def getFile(url):
    file_name = url.split('/')[-1]
    u = urllib.request.urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        f.write(buffer)
    f.close()
    print ("Sucessful to download" + " " + file_name)


root_url = 'http://pm.zjsti.gov.cn/tempublicfiles/'  #下载地址中相同的部分

raw_url = 'file:///E:/ZjuTH/Documents/pythonCode/pythontest.html'

html = getHtml(raw_url)
url_lst = getUrl(html)

os.mkdir('pdf_download')
os.chdir(os.path.join(os.getcwd(), 'pdf_download'))

for url in url_lst[:]:
    url = root_url + url+'/'+url+'.pdf'  #形成完整的下载地址
    getFile(url)


#333333333######################
import urllib.request 
import re 
import os 
#http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=000048&id=1422814 
#http://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESH_STOCK/2009/2009-3/2009-03-10/398698.PDF  
url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+'000048'+'/page_type/ndbg.phtml' 
req = urllib.request.Request(url) req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
page = urllib.request.urlopen(req) 
html = page.read().decode('utf-8') #'gb2312 
target = r'&id=[_0-9_]{6,7}' 
target_list = re.findall(target,html) 
print(target_list) 

import urllib.request 
import re 
import os 
os.mkdir('./000048') 
target_url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=000048'+'&id=712408' 
treq = urllib.request.Request(target_url) 
treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
tpage = urllib.request.urlopen(treq) 
thtml = tpage.read().decode('gbk') 
#print(thtml) 
file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml) 
print(file_url.group(0)) 
local = './'+'000048'+'/'+file_url.group(0).split("/")[-1]+'.pdf' 
urllib.request.urlretrieve(file_url.group(0),local,None)


import urllib.request 
import re 
import os 
url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+'000048'+'/page_type/ndbg.phtml' 
req = urllib.request.Request(url) 
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
page = urllib.request.urlopen(req) html = page.read().decode('gbk') 
target = r'&id=[_0-9_]{6,7}' 
target_list = re.findall(target,html) 
os.mkdir('./000048') 
for each in target_list:
 print(each)
 target_url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid=600616'+each 
 treq = urllib.request.Request(target_url) treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
 tpage = urllib.request.urlopen(treq) 
 thtml = tpage.read().decode('gbk') #print(thtml) 
 try: 
	file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml) 
	print(file_url.group(0)) 
	local = './000048/'+file_url.group(0).split("/")[-1]+'.pdf' #写入一个空文件站位，实际使用时使用urlretrieve可以下载文件 
	open(local, 'wb').write(b'success') 
	#urllib.request.urlretrieve(file_url.group(0),local,None) 
except: 
	print('失效')



import urllib.request 
import re 
import os 
f=open('stock_num.txt') 
stock = [] for line in f.readlines(): 
    #print(line,end = '') 
    line = line.replace('\n','') 
    stock.append(line) 
    #print(stock) 
    f.close() 
    #print(stock) 
    for each in stock: 
        url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'+each+'/page_type/ndbg.phtml' 
        req = urllib.request.Request(url) 
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
        page = urllib.request.urlopen(req) 
        try: 
            html = page.read().decode('gbk') 
            target = r'&id=[_0-9_]{6}' 
            target_list = re.findall(target,html) 
            os.mkdir('./'+each) 
            sid = each 
            #print(target_list) 
            for each in target_list: 
                #print(a) #print(each) 
                target_url='http://vip.stock.finance.sina.com.cn/corp/view/vCB_AllBulletinDetail.php?stockid='+sid+each 
                #print(target_url) 
                treq = urllib.request.Request(target_url) 
                treq.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
                tpage = urllib.request.urlopen(treq) 
                try: 
                    thtml = tpage.read().decode('gbk') 
                    #print(thtml) 
                    file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',thtml) 
                    try: 
                        #print(file_url.group(0)) 
                        local = './'+sid+'/'+file_url.group(0).split("/")[-1]+'.pdf' 
                        #调试用作文件占位 
                        # #open(local, 'wb').write(b'success') 
                        #print(local) 
                        urllib.request.urlretrieve(file_url.group(0),local,None) 
                    except: 
                        print('PDF失效;'+target_url) 
                except: 
                    print('年报下载页面编码错误;'+target_url) 
            except: 
                print('年报列表页面编码错误;'+url)